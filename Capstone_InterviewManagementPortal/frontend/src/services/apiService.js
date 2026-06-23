import axios from 'axios';

// Vite uses import.meta.env instead of process.env
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request Interceptor: Attach Basic Auth header if credentials exist
apiClient.interceptors.request.use(
    (config) => {
        const credentials = localStorage.getItem('basicAuth');
        if (credentials) {
            config.headers['Authorization'] = `Basic ${credentials}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response Interceptor: Handle global errors (e.g., 401 Unauthorized)
apiClient.interceptors.response.use(
    (response) => {
        return response.data;
    },
    (error) => {
        if (error.response) {
            if (error.response.status === 401) {
                // Clear storage and redirect to login on unauthorized
                localStorage.removeItem('basicAuth');
                localStorage.removeItem('userRole');
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;