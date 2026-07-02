import { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import apiClient, { clearAuthenticationData } from '../../services/apiService';

const ADMIN_ROLE = 'ADMIN';
const HR_ROLE = 'HR';
const INTERVIEWER_ROLE = 'INTERVIEWER';

/**
 * Render role-aware navigation for authenticated users.
 *
 * @returns {JSX.Element} Sidebar navigation and logout action.
 */
const Sidebar = () => {
    const role = localStorage.getItem('userRole');
    const navigate = useNavigate();
    const [isLoggingOut, setIsLoggingOut] = useState(false);
    const [logoutError, setLogoutError] = useState('');

    /**
     * Sign the user out without allowing duplicate requests or inconsistent auth state.
     */
    const handleLogout = async () => {
        if (isLoggingOut) {
            return;
        }

        setLogoutError('');
        setIsLoggingOut(true);

        try {
            if (!localStorage.getItem('basicAuth')) {
                clearAuthenticationData();
                navigate('/login', { replace: true });
                return;
            }

            await apiClient.post('/auth/logout');
            clearAuthenticationData();
            navigate('/login', { replace: true });
        } catch {
            setLogoutError('We could not sign you out right now. Please try again.');
        } finally {
            setIsLoggingOut(false);
        }
    };

    return (
        <div className="sidebar">
            <h3 className="sidebar-title">NucleusTeq Portal</h3>

            <ul className="nav-menu">
                <li><NavLink to="/dashboard" className="nav-item">Dashboard</NavLink></li>
                {(role === ADMIN_ROLE || role === HR_ROLE) && (
                    <li><NavLink to="/users" className="nav-item">Users</NavLink></li>
                )}
                {role === HR_ROLE && (
                    <>
                        <li><NavLink to="/jobs" className="nav-item">Jobs</NavLink></li>
                        <li><NavLink to="/candidates" className="nav-item">Candidates</NavLink></li>
                    </>
                )}
                {(role === HR_ROLE || role === INTERVIEWER_ROLE) && (
                    <li><NavLink to="/interviews" className="nav-item">Interviews</NavLink></li>
                )}
            </ul>

            {logoutError && <div className="error-text">{logoutError}</div>}

            <button
                onClick={handleLogout}
                className="logout-btn"
                disabled={isLoggingOut}
                aria-busy={isLoggingOut}
            >
                {isLoggingOut ? 'Logging out...' : 'Logout'}
            </button>
        </div>
    );
};

export default Sidebar;
