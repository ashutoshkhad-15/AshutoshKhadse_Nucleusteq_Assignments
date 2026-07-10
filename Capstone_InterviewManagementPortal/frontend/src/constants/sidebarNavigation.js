import { USER_ROLES } from './roles';
import { ROUTES } from './routes';

export const SIDEBAR_NAV_ITEMS = [
    { to: ROUTES.DASHBOARD, label: 'Dashboard', visibleRoles: null },
    { to: ROUTES.INTERVIEWS, label: 'Interviews', visibleRoles: [USER_ROLES.HR, USER_ROLES.ADMIN] },
    { to: ROUTES.INTERVIEW_ASSIGNED, label: 'Assigned Interviews', visibleRoles: [USER_ROLES.INTERVIEWER] },
    { to: ROUTES.USERS, label: 'Users', visibleRoles: [USER_ROLES.ADMIN] },
    { to: ROUTES.JOBS, label: 'Jobs', visibleRoles: [USER_ROLES.HR, USER_ROLES.ADMIN, USER_ROLES.INTERVIEWER] },
    { to: ROUTES.CANDIDATES, label: 'Candidates', visibleRoles: [USER_ROLES.ADMIN, USER_ROLES.HR] },
];
