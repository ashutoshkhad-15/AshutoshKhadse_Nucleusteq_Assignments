import apiClient from './apiService';
import { withSearchParam } from '../utils/requestParams';

const INTERVIEWS_BASE_PATH = '/interviews';

/**
 * Interview scheduling and feedback API operations backed by the shared authenticated client.
 */
export const interviewService = {
    /**
     * Fetch interviews with optional search and pagination.
     */
    async getAllInterviews(search = '', config = {}) {
        const response = await apiClient.get(`${INTERVIEWS_BASE_PATH}/`, withSearchParam(search, config));
        return response.data;
    },

    /**
     * Fetch a single interview by identifier.
     */
    async getInterviewById(interviewId, config = {}) {
        const response = await apiClient.get(`${INTERVIEWS_BASE_PATH}/${interviewId}`, config);
        return response.data.data;
    },

    /**
     * Create a new interview schedule.
     */
    async createInterview(interviewData) {
        const response = await apiClient.post(`${INTERVIEWS_BASE_PATH}/`, interviewData);
        return response.data.data;
    },

    /**
     * Update an interview schedule.
     */
    async updateInterview(interviewId, interviewData) {
        const response = await apiClient.patch(`${INTERVIEWS_BASE_PATH}/${interviewId}`, interviewData);
        return response.data.data;
    },

    /**
     * Submit interview feedback.
     */
    async submitFeedback(interviewId, feedbackData) {
        const response = await apiClient.post(`${INTERVIEWS_BASE_PATH}/${interviewId}/feedback`, feedbackData);
        return response.data.data;
    },

    /**
     * Load stored feedback for an interview.
     */
    async getFeedback(interviewId, config = {}) {
        const response = await apiClient.get(`${INTERVIEWS_BASE_PATH}/${interviewId}/feedback`, config);
        return response.data.data;
    },

    /**
     * Fetch interviews assigned to the current interviewer.
     */
    async getAssignedInterviews(config = {}) {
        const response = await apiClient.get(`${INTERVIEWS_BASE_PATH}/assigned`, config);
        return response.data;
    },

    /**
     * Fetch interviewer dropdown options.
     */
    async getInterviewers(search = '', config = {}) {
        const response = await apiClient.get(`${INTERVIEWS_BASE_PATH}/interviewers`, withSearchParam(search, config));
        return response.data;
    },

    /**
     * Fetch HR dashboard statistics.
     */
    async getHrDashboard(config = {}) {
        const response = await apiClient.get(`${INTERVIEWS_BASE_PATH}/dashboard/hr`, config);
        return response.data.data;
    },

    /**
     * Fetch admin dashboard statistics.
     */
    async getAdminDashboard(config = {}) {
        const response = await apiClient.get(`${INTERVIEWS_BASE_PATH}/dashboard/admin`, config);
        return response.data.data;
    },

    /**
     * Fetch interviewer dashboard statistics.
     */
    async getInterviewerDashboard(config = {}) {
        const response = await apiClient.get(`${INTERVIEWS_BASE_PATH}/dashboard/interviewer`, config);
        return response.data.data;
    },
};
