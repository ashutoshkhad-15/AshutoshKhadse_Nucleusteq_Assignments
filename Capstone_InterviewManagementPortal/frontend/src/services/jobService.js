import apiClient from './apiService';
import { API_PATHS } from '../constants/apiConstants';
import { withSearchParam } from '../utils/requestParams';

/**
 * Job description API operations backed by the shared authenticated client.
 */
export const jobService = {
    /**
     * Fetch all job descriptions.
     *
     * @param {object} [params={}] - Query parameters for filtering and search.
     * @param {object} [config={}] - Optional Axios request configuration.
     * @returns {Promise<Array>} Job records returned by the backend.
     */
    async getAllJobs(search = '', config = {}) {
        const response = await apiClient.get(`${API_PATHS.JOBS}/`, withSearchParam(search, config));
        return response.data;
    },

    /**
     * Fetch a single job description by identifier.
     *
     * @param {string} jobId - Job identifier.
     * @param {object} [config={}] - Optional Axios request configuration.
     * @returns {Promise<object>} Job record.
     */
    async getJobById(jobId, config = {}) {
        const response = await apiClient.get(`${API_PATHS.JOBS}/${jobId}`, config);
        return response.data.data;
    },

    /**
     * Create a new job description.
     *
     * @param {object} jobData - Job payload.
     * @returns {Promise<object>} Created job details.
     */
    async createJob(jobData) {
        const response = await apiClient.post(`${API_PATHS.JOBS}/`, jobData);
        return response.data.data;
    },

    /**
     * Update an existing job description.
     *
     * @param {string} jobId - Job identifier.
     * @param {object} updateData - Fields to update.
     * @returns {Promise<object>} Updated job details.
     */
    async updateJob(jobId, updateData) {
        const response = await apiClient.patch(`${API_PATHS.JOBS}/${jobId}`, updateData);
        return response.data.data;
    },
};
