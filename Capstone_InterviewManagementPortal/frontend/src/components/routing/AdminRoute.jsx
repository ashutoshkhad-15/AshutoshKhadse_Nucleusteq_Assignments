import { Navigate, Outlet } from 'react-router-dom';
import MainLayout from '../layout/MainLayout';
import { isAdmin, isAuthenticated } from '../../utils/session';

/**
 * Restrict access to administrative user-management routes.
 *
 * @returns {JSX.Element} Admin layout shell or a redirect for unauthorized users.
 */
const AdminRoute = () => {
    if (!isAuthenticated()) {
        return <Navigate to="/login" replace />;
    }

    if (!isAdmin()) {
        return <Navigate to="/dashboard" replace />;
    }

    return (
        <MainLayout>
            <Outlet />
        </MainLayout>
    );
};

export default AdminRoute;
