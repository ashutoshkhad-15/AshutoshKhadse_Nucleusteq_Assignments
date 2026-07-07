import apiClient from './apiService';

const CANDIDATES_BASE_PATH = '/candidates';

export const candidateService = {
    async getAllCandidates(search = '', config = {}) {
        const params = { ...(config.params || {}) };
        if (search?.trim()) params.search = search.trim();
        const response = await apiClient.get(`${CANDIDATES_BASE_PATH}/`, { ...config, params });
        return response.data;
    },

    async getCandidateById(candidateId, config = {}) {
        const response = await apiClient.get(`${CANDIDATES_BASE_PATH}/${candidateId}`, config);
        return response.data.data;
    },

    async createCandidate(candidateData) {
        const response = await apiClient.post(`${CANDIDATES_BASE_PATH}/`, candidateData);
        return response.data.data;
    },

    async updateCandidate(candidateId, updateData) {
        const response = await apiClient.patch(`${CANDIDATES_BASE_PATH}/${candidateId}`, updateData);
        return response.data.data;
    },

    async searchJobs(search = '', config = {}) {
        const params = { ...(config.params || {}) };
        if (search?.trim()) params.search = search.trim();
        const response = await apiClient.get(`${CANDIDATES_BASE_PATH}/jobs/search`, { ...config, params });
        return response.data;
    },

    /**
     * Upload a PDF resume for a candidate.
     */
    async uploadResume(candidateId, formData, config = {}) {
        const response = await apiClient.post(`${CANDIDATES_BASE_PATH}/${candidateId}/resume`, formData, config);
        return response.data.data;
    },

    /**
     * Fetch stored resume metadata and PDF payload for a candidate.
     */
    async getResume(candidateId, config = {}) {
        const response = await apiClient.get(`${CANDIDATES_BASE_PATH}/${candidateId}/resume`, config);
        return response.data.data;
    },

    /**
     * Update the candidate status.
     */
    async updateCandidateStatus(candidateId, status, config = {}) {
        const params = { ...(config.params || {}), status };
        const response = await apiClient.patch(`${CANDIDATES_BASE_PATH}/${candidateId}/status`, null, {
            ...config,
            params,
        });
        return response.data.data;
    },

    /**
     * Fetch candidate status history.
     */
    async getCandidateStatusHistory(candidateId, config = {}) {
        const response = await apiClient.get(`${CANDIDATES_BASE_PATH}/${candidateId}/status-history`, config);
        return response.data.data;
    },
};
