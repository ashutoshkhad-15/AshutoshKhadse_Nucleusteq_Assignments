import apiClient from '../services/apiService';
import { clearSession } from './session';

export const signOut = async () => {
    await apiClient.post('/auth/logout');
    clearSession();
};
