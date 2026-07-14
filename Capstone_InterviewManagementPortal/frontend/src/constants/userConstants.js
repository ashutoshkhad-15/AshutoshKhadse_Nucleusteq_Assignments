import { USER_ROLES } from './roles';

export const DEFAULT_ADMIN_EMAIL = 'admin@nucleusteq.com';

export const USER_ROLE_OPTIONS = [
    { value: USER_ROLES.ADMIN, label: 'Admin' },
    { value: USER_ROLES.HR, label: 'HR' },
    { value: USER_ROLES.INTERVIEWER, label: 'Interviewer' },
];
