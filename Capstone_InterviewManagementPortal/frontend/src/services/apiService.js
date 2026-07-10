import axios from 'axios';
import { clearSession, getStoredAuthToken } from '../utils/session';

const AUTH_LOGIN_PATH = '/auth/login';

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
});

const isFormData = (value) => typeof FormData !== 'undefined' && value instanceof FormData;

/**
 * Attach the persisted Basic Auth token to authenticated API requests.
 */
const attachAuthHeader = (config) => {
    const token = getStoredAuthToken();
    const headers = config.headers || {};

    if (token) {
        headers.Authorization = `Basic ${token}`;
    }

    if (isFormData(config.data)) {
        delete headers['Content-Type'];
        delete headers['content-type'];
    }

    config.headers = headers;

    return config;
};

/**
 * Clear client-side session state when an authenticated request expires.
 */
const handleUnauthorizedResponse = (error) => {
    const requestUrl = error.config?.url || '';
    const isLoginRequest = requestUrl.includes(AUTH_LOGIN_PATH);

    if (error.response?.status === 401 && !isLoginRequest) {
        clearSession();
        window.location.href = '/login';
    }

    return Promise.reject(error);
};

apiClient.interceptors.request.use(attachAuthHeader, Promise.reject);
apiClient.interceptors.response.use(
    (response) => response,
    handleUnauthorizedResponse
);

export default apiClient;
