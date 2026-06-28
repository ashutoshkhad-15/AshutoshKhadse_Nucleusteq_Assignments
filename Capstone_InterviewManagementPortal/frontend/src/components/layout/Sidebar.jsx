import { NavLink, useNavigate } from 'react-router-dom';
import apiClient from '../../services/apiService';

const ADMIN_ROLE = 'ADMIN';
const HR_ROLE = 'HR';
const INTERVIEWER_ROLE = 'INTERVIEWER';

/**
 * Render role-aware navigation for authenticated users.
 *
 * @param {object} props
 * @param {boolean} props.isCollapsed - Determines if the sidebar is shrunk.
 * @param {function} props.setIsCollapsed - Toggles the sidebar state.
 * @returns {JSX.Element} Sidebar navigation and logout action.
 */
const Sidebar = ({ isCollapsed, setIsCollapsed }) => {
    const role = localStorage.getItem('userRole');
    const navigate = useNavigate();

    const navItems = [
        { to: '/dashboard', label: 'Dashboard', shortLabel: 'DB', visible: true },
        { to: '/users', label: 'Users', shortLabel: 'US', visible: role === ADMIN_ROLE },
        { to: '/jobs', label: 'Jobs', shortLabel: 'JB', visible: role === HR_ROLE },
        { to: '/candidates', label: 'Candidates', shortLabel: 'CD', visible: role === HR_ROLE },
        {
            to: '/interviews',
            label: 'Interviews',
            shortLabel: 'IN',
            visible: role === HR_ROLE || role === INTERVIEWER_ROLE,
        },
    ];

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
        <div className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
            <div className="sidebar-header">
                {!isCollapsed && (
                    <div className="sidebar-brand">
                        <p className="sidebar-eyebrow">Admin Portal</p>
                        <h3 className="sidebar-title">NucleusTeq</h3>
                    </div>
                )}
                <button
                    className="toggle-btn"
                    onClick={() => setIsCollapsed(!isCollapsed)}
                    title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
                    aria-label={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
                >
                    {isCollapsed ? '>' : '<'}
                </button>
            </div>

            <ul className="nav-menu">
                {navItems.filter((item) => item.visible).map((item) => (
                    <li key={item.to}>
                        <NavLink to={item.to} className="nav-item">
                            <span className="nav-icon" aria-hidden="true">{item.shortLabel}</span>
                            {!isCollapsed && <span className="nav-text">{item.label}</span>}
                        </NavLink>
                    </li>
                ))}
            </ul>

            <button onClick={handleLogout} className="logout-btn">
                <span className="nav-icon" aria-hidden="true">LO</span>
                {!isCollapsed && <span className="nav-text">Logout</span>}
            </button>
        </div>
    );
};

export default Sidebar;
