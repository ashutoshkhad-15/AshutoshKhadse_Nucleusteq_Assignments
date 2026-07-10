import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import { useEffect } from 'react';
import MainLayout from './components/layout/MainLayout';
import AdminRoute from './components/routing/AdminRoute';
import DashboardScreen from './pages/DashboardScreen';
import InterviewListScreen from './pages/InterviewListScreen';
import InterviewDetailsScreen from './pages/InterviewDetailsScreen';
import ScheduleInterviewScreen from './pages/ScheduleInterviewScreen';
import EditInterviewScreen from './pages/EditInterviewScreen';
import AssignedInterviewsScreen from './pages/AssignedInterviewsScreen';
import SubmitFeedbackScreen from './pages/SubmitFeedbackScreen';
import CreateJobScreen from './pages/CreateJobScreen';
import CreateCandidateScreen from './pages/CreateCandidateScreen';
import CreateUserScreen from './pages/CreateUserScreen';
import CandidateDetailsScreen from './pages/CandidateDetailsScreen';
import CandidateListScreen from './pages/CandidateListScreen';
import EditCandidateScreen from './pages/EditCandidateScreen';
import EditJobScreen from './pages/EditJobScreen';
import EditUserScreen from './pages/EditUserScreen';
import JobDetailsScreen from './pages/JobDetailsScreen';
import JobListScreen from './pages/JobListScreen';
import Login from './pages/Login';
import ResetPassword from './pages/ResetPassword';
import CandidateResumePreviewScreen from './pages/CandidateResumePreviewScreen';
import CandidateStatusHistoryScreen from './pages/CandidateStatusHistoryScreen';
import UserListScreen from './pages/UserListScreen';
import { USER_ROLES } from './constants/roles';
import { ROUTES } from './constants/routes';
import { getStoredAuthToken, getStoredUserRole, hasAnyRole } from './utils/session';

const NotFound = () => <h2>Page not found</h2>;

/**
 * Protects pages that require an authenticated browser session.
 *
 * @param {object} props - Component props.
 * @param {React.ReactNode} props.children - Protected page content.
 * @returns {JSX.Element} Protected content or login redirect.
 */
const ProtectedRoute = ({ children }) => (getStoredAuthToken() ? children : <Navigate to={ROUTES.LOGIN} replace />);

/**
 * Keeps authenticated users out of public authentication pages.
 *
 * @param {object} props - Component props.
 * @param {React.ReactNode} props.children - Public page content.
 * @returns {JSX.Element} Public content or dashboard redirect.
 */
const PublicRoute = ({ children }) => (getStoredAuthToken() ? <Navigate to={ROUTES.DASHBOARD} replace /> : children);

/**
 * Restrict protected routes to specific user roles.
 *
 * @param {object} props - Component props.
 * @param {Array<string>} props.allowedRoles - Roles allowed to access the route.
 * @param {React.ReactNode} props.children - Protected page content.
 * @returns {JSX.Element} Role-allowed content or redirect.
 */
const RoleRoute = ({ allowedRoles, children }) => {
    const auth = getStoredAuthToken();
    const role = getStoredUserRole();

    if (!auth || !role) return <Navigate to={ROUTES.LOGIN} replace />;
    if (!hasAnyRole(allowedRoles)) return <Navigate to={ROUTES.DASHBOARD} replace />;

    return <MainLayout>{children}</MainLayout>;
};

/**
 * Compose the portal routes and shared access guards.
 *
 * @returns {JSX.Element} Application routing shell.
 */
function App() {
    useEffect(() => {
        document.title = 'TalentFlow Interview Portal';
    }, []);

    return (
        <Router>
            <Routes>
                <Route path={ROUTES.ROOT} element={<Navigate to={ROUTES.DASHBOARD} />} />
                <Route
                    path={ROUTES.LOGIN}
                    element={(
                        <PublicRoute>
                            <Login />
                        </PublicRoute>
                    )}
                />
                <Route
                    path={ROUTES.RESET_PASSWORD}
                    element={(
                        <PublicRoute>
                            <ResetPassword />
                        </PublicRoute>
                    )}
                />
                <Route
                    path={ROUTES.DASHBOARD}
                    element={(
                        <ProtectedRoute>
                            <MainLayout>
                                <DashboardScreen />
                            </MainLayout>
                        </ProtectedRoute>
                    )}
                />
                <Route element={<AdminRoute />}>
                    <Route path={ROUTES.USERS} element={<UserListScreen />} />
                    <Route path={ROUTES.USER_CREATE} element={<CreateUserScreen />} />
                    <Route path={ROUTES.USER_EDIT} element={<EditUserScreen />} />
                </Route>
                <Route
                    path={ROUTES.CANDIDATES}
                    element={(
                        <RoleRoute allowedRoles={['HR', 'ADMIN', 'INTERVIEWER']}>
                            <CandidateListScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.CANDIDATE_CREATE}
                    element={(
                        <RoleRoute allowedRoles={['HR']}>
                            <CreateCandidateScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.CANDIDATE_DETAILS}
                    element={(
                        <RoleRoute allowedRoles={['HR', 'ADMIN', 'INTERVIEWER']}>
                            <CandidateDetailsScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.CANDIDATE_RESUME}
                    element={(
                        <RoleRoute allowedRoles={['HR', 'ADMIN', 'INTERVIEWER']}>
                            <CandidateResumePreviewScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.CANDIDATE_STATUS_HISTORY}
                    element={(
                        <RoleRoute allowedRoles={['HR', 'ADMIN', 'INTERVIEWER']}>
                            <CandidateStatusHistoryScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.CANDIDATE_EDIT}
                    element={(
                        <RoleRoute allowedRoles={['HR']}>
                            <EditCandidateScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.JOBS}
                    element={(
                        <RoleRoute allowedRoles={['HR', 'ADMIN', 'INTERVIEWER']}>
                            <JobListScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.JOB_DETAILS}
                    element={(
                        <RoleRoute allowedRoles={['HR', 'ADMIN', 'INTERVIEWER']}>
                            <JobDetailsScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.JOB_CREATE}
                    element={(
                        <RoleRoute allowedRoles={['HR']}>
                            <CreateJobScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.JOB_EDIT}
                    element={(
                        <RoleRoute allowedRoles={['HR']}>
                            <EditJobScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.INTERVIEWS}
                    element={(
                        <RoleRoute allowedRoles={[USER_ROLES.HR, USER_ROLES.ADMIN, USER_ROLES.INTERVIEWER]}>
                            <InterviewListScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.INTERVIEW_SCHEDULE}
                    element={(
                        <RoleRoute allowedRoles={[USER_ROLES.HR, USER_ROLES.ADMIN]}>
                            <ScheduleInterviewScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.INTERVIEW_EDIT}
                    element={(
                        <RoleRoute allowedRoles={[USER_ROLES.HR, USER_ROLES.ADMIN]}>
                            <EditInterviewScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.INTERVIEW_ASSIGNED}
                    element={(
                        <RoleRoute allowedRoles={[USER_ROLES.INTERVIEWER]}>
                            <AssignedInterviewsScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.INTERVIEW_DETAILS}
                    element={(
                        <RoleRoute allowedRoles={[USER_ROLES.HR, USER_ROLES.ADMIN, USER_ROLES.INTERVIEWER]}>
                            <InterviewDetailsScreen />
                        </RoleRoute>
                    )}
                />
                <Route
                    path={ROUTES.INTERVIEW_FEEDBACK}
                    element={(
                        <RoleRoute allowedRoles={[USER_ROLES.HR, USER_ROLES.ADMIN, USER_ROLES.INTERVIEWER]}>
                            <SubmitFeedbackScreen />
                        </RoleRoute>
                    )}
                />
                <Route path="*" element={<NotFound />} />
            </Routes>
        </Router>
    );
}

export default App;
