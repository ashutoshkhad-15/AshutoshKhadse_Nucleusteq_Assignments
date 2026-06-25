import axios from 'axios';

/**
 * Base URL for versioned backend API requests.
 *
 * Vite exposes environment variables through import.meta.env, with localhost
 * used as the development fallback.
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Shared Axios client for Interview Management Portal API calls.
 *
 * The client returns response payloads directly and centralizes authentication
 * headers plus unauthorized-session cleanup.
 */
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

apiClient.interceptors.request.use(
    (config) => {
        const credentials = localStorage.getItem('basicAuth');
        if (credentials) {
            // Attach credentials only when the session has stored Basic Auth data.
            config.headers['Authorization'] = `Basic ${credentials}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

apiClient.interceptors.response.use(
    (response) => {
        return response.data;
    },
    (error) => {
        if (error.response) {
            if (error.response.status === 401) {
                // Clear stale credentials before redirecting unauthorized users.
                localStorage.removeItem('basicAuth');
                localStorage.removeItem('userRole');
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;
