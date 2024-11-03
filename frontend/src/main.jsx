import React from 'react';
import ReactDOM from 'react-dom/client'; // Import from 'react-dom/client'
import App from './App';
import { Auth0Provider } from '@auth0/auth0-react';

const domain = import.meta.env.VITE_AUTH0_DOMAIN; // Accessing the domain from env
const clientId = import.meta.env.VITE_AUTH0_CLIENT_ID; // Accessing the client ID from env

const root = ReactDOM.createRoot(document.getElementById('root')); // Create a root

root.render(
    <Auth0Provider
        domain={domain}
        clientId={clientId}
        redirectUri={window.location.origin}
        audience={import.meta.env.VITE_API_AUDIENCE} // Accessing the API audience from env
    >
        <App />
    </Auth0Provider>
);
