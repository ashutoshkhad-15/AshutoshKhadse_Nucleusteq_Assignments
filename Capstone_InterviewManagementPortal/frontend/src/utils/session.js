import { USER_ROLES } from '../constants/roles';

const BASIC_AUTH_STORAGE_KEY = 'basicAuth';
const USER_ROLE_STORAGE_KEY = 'userRole';

export const getStoredAuthToken = () => localStorage.getItem(BASIC_AUTH_STORAGE_KEY);

export const getStoredUserRole = () => localStorage.getItem(USER_ROLE_STORAGE_KEY);

export const isAuthenticated = () => Boolean(getStoredAuthToken());

export const hasAnyRole = (allowedRoles = []) => allowedRoles.includes(getStoredUserRole());

export const isAdmin = () => getStoredUserRole() === USER_ROLES.ADMIN;
export const isHr = () => getStoredUserRole() === USER_ROLES.HR;
export const isInterviewer = () => getStoredUserRole() === USER_ROLES.INTERVIEWER;

export const clearSession = () => {
    localStorage.removeItem(BASIC_AUTH_STORAGE_KEY);
    localStorage.removeItem(USER_ROLE_STORAGE_KEY);
    sessionStorage.removeItem(BASIC_AUTH_STORAGE_KEY);
    sessionStorage.removeItem(USER_ROLE_STORAGE_KEY);
};

