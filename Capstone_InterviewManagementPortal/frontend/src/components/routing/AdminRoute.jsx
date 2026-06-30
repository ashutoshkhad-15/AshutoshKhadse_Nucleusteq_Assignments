import { Navigate, Outlet } from 'react-router-dom';
import MainLayout from '../layout/MainLayout';

/**
 * Restrict access to administrative user-management routes.
 *
 * @returns {JSX.Element} Admin layout shell or a redirect for unauthorized users.
 */
const AdminRoute = () => {
    const role = localStorage.getItem('userRole');
    const auth = localStorage.getItem('basicAuth');

    if (!role || !auth) {
        return <Navigate to="/login" replace />;
    }

    if (role !== 'ADMIN') {
        return <Navigate to="/dashboard" replace />;
    }

    return (
        <MainLayout>
            <Outlet />
        </MainLayout>
    );
};

export default AdminRoute;
