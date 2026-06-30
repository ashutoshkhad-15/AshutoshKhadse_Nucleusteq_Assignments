import axios from 'axios';

const AUTH_LOGIN_PATH = '/auth/login';
const BASIC_AUTH_STORAGE_KEY = 'basicAuth';
const USER_ROLE_STORAGE_KEY = 'userRole';

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Attach the persisted Basic Auth token to authenticated API requests.
 */
const attachAuthHeader = (config) => {
    const token = localStorage.getItem(BASIC_AUTH_STORAGE_KEY);

    if (token) {
        config.headers.Authorization = `Basic ${token}`;
    }

    return config;
};

/**
 * Clear client-side session state when an authenticated request expires.
 */
const handleUnauthorizedResponse = (error) => {
    const requestUrl = error.config?.url || '';
    const isLoginRequest = requestUrl.includes(AUTH_LOGIN_PATH);

    if (error.response?.status === 401 && !isLoginRequest) {
        localStorage.removeItem(BASIC_AUTH_STORAGE_KEY);
        localStorage.removeItem(USER_ROLE_STORAGE_KEY);
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
