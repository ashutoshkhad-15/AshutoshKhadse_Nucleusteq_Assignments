import apiClient from './apiService';
import { API_PATHS } from '../constants/apiConstants';

/**
 * User management API operations backed by the shared authenticated client.
 */
export const userService = {
    /**
     * Fetch all application users or perform a backend search.
     *
     * @param {string} [search=''] - Optional search term for the server-side filter.
     * @param {object} [config={}] - Optional Axios request configuration.
     * @returns {Promise<Array>} User records returned by the backend.
     */
    async getAllUsers(search = '', config = {}) {
        const params = {};

        if (search?.trim()) {
            params.search = search.trim();
        }

        const requestConfig = {
            ...config,
            params: {
                ...(config.params || {}),
                ...params,
            },
        };

        const response = await apiClient.get(`${API_PATHS.USERS}/`, requestConfig);
        return response.data;
    },

    /**
     * Fetch a single user by identifier.
     *
     * @param {string} userId - User identifier.
     * @returns {Promise<object>} User record.
     */
    async getUserById(userId, config = {}) {
        const response = await apiClient.get(`${API_PATHS.USERS}/${userId}`, config);
        return response.data.data;
    },

    /**
     * Create a new user account.
     *
     * @param {{ email: string, role: string }} userData - User payload.
     * @returns {Promise<object>} Created user details.
     */
    async createUser(userData) {
        const response = await apiClient.post(`${API_PATHS.USERS}/`, userData);
        return response.data.data;
    },

    /**
     * Update a user account.
     *
     * @param {string} userId - User identifier.
     * @param {{ role?: string, is_active?: boolean }} updateData - Fields to update.
     * @returns {Promise<object>} Updated user details.
     */
    async updateUser(userId, updateData) {
        const payload = { ...updateData };
        if (payload.name !== undefined && typeof payload.name === 'string') {
            payload.name = payload.name.trim();
        }
        if (payload.email !== undefined && typeof payload.email === 'string') {
            payload.email = payload.email.trim();
        }
        const response = await apiClient.patch(`${API_PATHS.USERS}/${userId}`, payload);
        return response.data.data;
    },

    /**
     * Disable a user account.
     *
     * @param {string} userId - User identifier.
     * @returns {Promise<string>} Success message from the backend.
     */
    async disableUser(userId) {
        const response = await apiClient.patch(`${API_PATHS.USERS}/${userId}/disable`);
        return response.data.message;
    },
};
