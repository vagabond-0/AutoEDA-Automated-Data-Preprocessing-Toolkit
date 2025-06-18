import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from './components/theme-provider.jsx';
import { Auth0Provider } from '@auth0/auth0-react';

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
      <Auth0Provider
        domain="dev-43q1ylsndoglcjlk.us.auth0.com"
        clientId="U2SKgQsmtwhSEjNuMHpVLpOZbdYCiiQy"
        authorizationParams={{
          redirect_uri: window.location.origin
        }}
      >
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <App />
    </ThemeProvider>
      </Auth0Provider>
  </BrowserRouter>
);
