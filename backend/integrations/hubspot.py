import json
import secrets
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import asyncio
import base64
import requests
from integrations.integration_item import IntegrationItem

from redis_client import add_key_value_redis, get_value_redis, delete_key_redis

CLIENT_ID = 'bb4e938f-d960-497f-9871-bf92191b2044'
CLIENT_SECRET = 'e5e8a435-ff32-431c-a6ab-a79d1a3354b5'
REDIRECT_URI = 'http://localhost:8000/integrations/hubspot/oauth2callback'
AUTHORIZATION_URL = 'https://app.hubspot.com/oauth/authorize'
SCOPE = 'crm.objects.contacts.read crm.schemas.contacts.read'


async def authorize_hubspot(user_id, org_id):
    state_data = {
        'state': secrets.token_urlsafe(32),
        'user_id': user_id,
        'org_id': org_id
    }
    encoded_state = base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode()
    await add_key_value_redis(f'hubspot_state:{org_id}:{user_id}', json.dumps(state_data), expire=600)
    
    auth_url = f'{AUTHORIZATION_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}&state={encoded_state}'
    return auth_url

async def oauth2callback_hubspot(request: Request):
    if request.query_params.get('error'):
        raise HTTPException(status_code=400, detail=request.query_params.get('error'))
    
    code = request.query_params.get('code')
    encoded_state = request.query_params.get('state')
    state_data = json.loads(base64.urlsafe_b64decode(encoded_state).decode())
    
    original_state = state_data.get('state')
    user_id = state_data.get('user_id')
    org_id = state_data.get('org_id')
    
    saved_state = await get_value_redis(f'hubspot_state:{org_id}:{user_id}')
    if not saved_state or original_state != json.loads(saved_state).get('state'):
        raise HTTPException(status_code=400, detail='State does not match.')

    async with httpx.AsyncClient() as client:
        response, _ = await asyncio.gather(
            client.post(
                'https://api.hubapi.com/oauth/v1/token',
                data={
                    'grant_type': 'authorization_code',
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'redirect_uri': REDIRECT_URI,
                    'code': code
                }
            ),
            delete_key_redis(f'hubspot_state:{org_id}:{user_id}')
        )
        
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail='Failed to get access token')
    
    await add_key_value_redis(f'hubspot_credentials:{org_id}:{user_id}', json.dumps(response.json()), expire=600)
    
    close_window_script = """
    <html>
        <script>
            window.close();
        </script>
    </html>
    """
    return HTMLResponse(content=close_window_script)

async def get_hubspot_credentials(user_id, org_id):
    credentials = await get_value_redis(f'hubspot_credentials:{org_id}:{user_id}')
    if not credentials:
        raise HTTPException(status_code=400, detail='No credentials found.')
    credentials = json.loads(credentials)
    await delete_key_redis(f'hubspot_credentials:{org_id}:{user_id}')
    return credentials

async def get_items_hubspot(credentials):
    credentials = json.loads(credentials)
    access_token = credentials.get('access_token')
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get('https://api.hubapi.com/crm/v3/objects/contacts', headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail='Failed to fetch HubSpot contacts')
        
    results = response.json().get('results', [])
    list_of_integration_item_metadata = []
    
    for result in results:
        list_of_integration_item_metadata.append(
            IntegrationItem(
                id=str(result.get('id')),
                type='contact',
                name=f"{result.get('properties', {}).get('firstname', '')} {result.get('properties', {}).get('lastname', '')}".strip(),
                creation_time=result.get('createdAt'),
                last_modified_time=result.get('updatedAt'),
                url=f"https://app.hubspot.com/contacts/{result.get('id')}"
            )
        )
    
    print(f'HubSpot items: {list_of_integration_item_metadata}')
    return list_of_integration_item_metadata