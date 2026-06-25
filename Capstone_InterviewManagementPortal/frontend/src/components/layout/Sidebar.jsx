import { NavLink, useNavigate } from 'react-router-dom';
import apiClient from '../../services/apiService';

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

    const handleLogout = async () => {
        try {
            await apiClient.post('/auth/logout');
        } catch {
            // Local session cleanup must still run if the backend logout request fails.
            console.warn('Backend logout failed, clearing local session anyway.');
        } finally {
            localStorage.removeItem('basicAuth');
            localStorage.removeItem('userRole');
            navigate('/login');
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

            <button onClick={handleLogout} className="logout-btn">
                Logout
            </button>
        </div>
    );
};

export default Sidebar;
