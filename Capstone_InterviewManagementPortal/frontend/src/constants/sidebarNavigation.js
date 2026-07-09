import { USER_ROLES } from './roles';

export const SIDEBAR_NAV_ITEMS = [
    { to: '/dashboard', label: 'Dashboard', visibleRoles: null },
    { to: '/users', label: 'Users', visibleRoles: [USER_ROLES.ADMIN] },
    { to: '/jobs', label: 'Jobs', visibleRoles: [USER_ROLES.HR, USER_ROLES.ADMIN, USER_ROLES.INTERVIEWER] },
    { to: '/candidates', label: 'Candidates', visibleRoles: [USER_ROLES.ADMIN, USER_ROLES.HR] },
];
