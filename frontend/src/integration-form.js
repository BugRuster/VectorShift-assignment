import React, { useState } from 'react';
import {
    Box,
    Autocomplete,
    TextField,
    Paper,
    Typography,
    Container,
} from '@mui/material';
import { AirtableIntegration } from './integrations/airtable';
import { NotionIntegration } from './integrations/notion';
import { HubSpotIntegration } from './integrations/hubspot';
import { DataForm } from './data-form';

const integrationMapping = {
    'Notion': NotionIntegration,
    'Airtable': AirtableIntegration,
    'HubSpot': HubSpotIntegration,
};

export const IntegrationForm = () => {
    const [integrationParams, setIntegrationParams] = useState({});
    const [user, setUser] = useState('TestUser');
    const [org, setOrg] = useState('TestOrg');
    const [currType, setCurrType] = useState(null);
    const CurrIntegration = integrationMapping[currType];

    return (
        <Container maxWidth="md" sx={{ py: 4 }}>
            <Box display='flex' flexDirection='column' gap={3}>
                <Paper elevation={3} sx={{ p: 3, backgroundColor: '#f8f9fa' }}>
                    <Typography variant="h5" gutterBottom color="primary" sx={{ mb: 3 }}>
                        Integration Configuration
                    </Typography>
                    
                    <Box display='flex' flexDirection='column' gap={2}>
                        <TextField
                            label="User"
                            value={user}
                            onChange={(e) => setUser(e.target.value)}
                            fullWidth
                            sx={{ backgroundColor: 'white' }}
                        />
                        <TextField
                            label="Organization"
                            value={org}
                            onChange={(e) => setOrg(e.target.value)}
                            fullWidth
                            sx={{ backgroundColor: 'white' }}
                        />
                        <Autocomplete
                            id="integration-type"
                            options={Object.keys(integrationMapping)}
                            value={currType}
                            onChange={(e, value) => setCurrType(value)}
                            renderInput={(params) => (
                                <TextField 
                                    {...params} 
                                    label="Integration Type"
                                    sx={{ backgroundColor: 'white' }}
                                />
                            )}
                        />
                    </Box>
                </Paper>

                {currType && (
                    <Paper elevation={3} sx={{ p: 3, backgroundColor: '#f8f9fa' }}>
                        <Typography variant="h6" gutterBottom color="primary" sx={{ mb: 3 }}>
                            {currType} Integration
                        </Typography>
                        <CurrIntegration 
                            user={user} 
                            org={org} 
                            integrationParams={integrationParams} 
                            setIntegrationParams={setIntegrationParams} 
                        />
                    </Paper>
                )}

                {integrationParams?.credentials && (
                    <DataForm 
                        integrationType={integrationParams?.type} 
                        credentials={integrationParams?.credentials} 
                    />
                )}
            </Box>
        </Container>
    );
}