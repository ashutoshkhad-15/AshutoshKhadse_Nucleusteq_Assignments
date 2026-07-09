import apiClient, { clearAuthenticationData } from '../services/apiService';

export const signOut = async () => {
    await apiClient.post('/auth/logout');
    clearAuthenticationData();
};
