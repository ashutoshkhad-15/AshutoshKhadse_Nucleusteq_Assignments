import apiClient from './apiService';
import { API_PATHS } from '../constants/apiConstants';
import { withSearchParam } from '../utils/requestParams';

export const candidateService = {
    async getAllCandidates(search = '', config = {}) {
        const response = await apiClient.get(`${API_PATHS.CANDIDATES}/`, withSearchParam(search, config));
        return response.data;
    },

    async getCandidateById(candidateId, config = {}) {
        const response = await apiClient.get(`${API_PATHS.CANDIDATES}/${candidateId}`, config);
        return response.data.data;
    },

    async createCandidate(candidateData) {
        const response = await apiClient.post(`${API_PATHS.CANDIDATES}/`, candidateData);
        return response.data.data;
    },

    async updateCandidate(candidateId, updateData) {
        const response = await apiClient.patch(`${API_PATHS.CANDIDATES}/${candidateId}`, updateData);
        return response.data.data;
    },

    async searchJobs(search = '', config = {}) {
        const response = await apiClient.get(`${API_PATHS.CANDIDATES}/jobs/search`, withSearchParam(search, config));
        return response.data;
    },

    /**
     * Upload a PDF resume for a candidate.
     */
    async uploadResume(candidateId, formData, config = {}) {
        const response = await apiClient.post(`${API_PATHS.CANDIDATES}/${candidateId}/resume`, formData, config);
        return response.data.data;
    },

    /**
     * Fetch stored resume metadata and PDF payload for a candidate.
     */
    async getResume(candidateId, config = {}) {
        const response = await apiClient.get(`${API_PATHS.CANDIDATES}/${candidateId}/resume`, config);
        return response.data.data;
    },

    /**
     * Update the candidate status.
     */
    async updateCandidateStatus(candidateId, status, config = {}) {
        const params = { ...(config.params || {}), status };
        const response = await apiClient.patch(`${API_PATHS.CANDIDATES}/${candidateId}/status`, null, {
            ...config,
            params,
        });
        return response.data.data;
    },

    /**
     * Fetch candidate status history.
     */
    async getCandidateStatusHistory(candidateId, config = {}) {
        const response = await apiClient.get(`${API_PATHS.CANDIDATES}/${candidateId}/status-history`, config);
        return response.data.data;
    },
};
