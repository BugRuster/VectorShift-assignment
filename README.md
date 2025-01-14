# VectorShift Technical Assessment

This project implements a HubSpot integration using FastAPI for the backend and React for the frontend. The application allows users to connect to their HubSpot account via OAuth and fetch contact data.

## Prerequisites

- Python 3.8 or higher
- Node.js and npm
- Redis server
- HubSpot developer account

## Installation & Setup

### 1. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # For Unix/MacOS
# OR
.\venv\Scripts\activate  # For Windows
```

Install dependencies:

```bash
pip install fastapi uvicorn httpx redis kombu requests python-multipart
```

### 2. Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

### 3. Redis Setup

Start Redis server:

```bash
redis-server
```

## Running the Application

1. Start the backend server (in backend directory):

```bash
uvicorn main:app --reload
```

2. Start the frontend development server (in frontend directory):

```bash
export NODE_OPTIONS=--openssl-legacy-provider
npm start
```

The application will be available at:

- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Features

- OAuth integration with HubSpot
- Contact data fetching
- Data display and management
- Copy functionality for fetched data
- Clear data option

## File Structure

```
├── backend/
│   ├── integrations/
│   │   ├── hubspot.py      # HubSpot integration implementation
│   │   ├── airtable.py     # Pre-built Airtable integration
│   │   └── notion.py       # Pre-built Notion integration
│   ├── main.py             # FastAPI main application
│   └── redis_client.py     # Redis connection handling
└── frontend/
    ├── src/
    │   ├── integrations/
    │   │   ├── hubspot.js  # HubSpot frontend component
    │   │   ├── airtable.js # Airtable component
    │   │   └── notion.js   # Notion component
    │   ├── App.js
    │   ├── data-form.js    # Data display component
    │   └── integration-form.js # Main form component
    └── package.json
```

## Usage

1. Open the application in your browser
2. Enter test user and organization details
3. Select HubSpot from the integration dropdown
4. Click "Connect to HubSpot" to start OAuth flow
5. After successful connection, use "Load Data" to fetch contacts
6. Use "Copy Data" to copy the fetched data
7. Use "Clear Data" to reset the display

## Error Handling

The application includes error handling for:

- OAuth flow failures
- API call errors
- Connection issues
- Data loading problems

Each error will display an appropriate message to the user.
