import apiClient from './apiService';

const USERS_BASE_PATH = '/users';

/**
 * User management API operations backed by the shared authenticated client.
 */
export const userService = {
    /**
     * Fetch all application users.
     *
     * @returns {Promise<Array>} User records returned by the backend.
     */
    async getAllUsers() {
        const response = await apiClient.get(`${USERS_BASE_PATH}/`);
        return response.data.data;
    },

    /**
     * Fetch a single user by identifier.
     *
     * @param {string} userId - User identifier.
     * @returns {Promise<object>} User record.
     */
    async getUserById(userId) {
        const response = await apiClient.get(`${USERS_BASE_PATH}/${userId}`);
        return response.data.data;
    },

    /**
     * Create a new user account.
     *
     * @param {{ email: string, role: string }} userData - User payload.
     * @returns {Promise<object>} Created user details.
     */
    async createUser(userData) {
        const response = await apiClient.post(`${USERS_BASE_PATH}/`, userData);
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
        const response = await apiClient.patch(`${USERS_BASE_PATH}/${userId}`, updateData);
        return response.data.data;
    },

    /**
     * Disable a user account.
     *
     * @param {string} userId - User identifier.
     * @returns {Promise<string>} Success message from the backend.
     */
    async disableUser(userId) {
        const response = await apiClient.patch(`${USERS_BASE_PATH}/${userId}/disable`);
        return response.data.message;
    },
};
