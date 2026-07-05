import { BriefcaseBusiness, ChevronLeft, ChevronRight, LayoutDashboard, LogOut, ShieldUser, Users } from 'lucide-react';
import { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import apiClient, { clearAuthenticationData } from '../../services/apiService';

const ADMIN_ROLE = 'ADMIN';
const HR_ROLE = 'HR';
const INTERVIEWER_ROLE = 'INTERVIEWER';

const Sidebar = ({ isCollapsed, setIsCollapsed }) => {
    const role = localStorage.getItem('userRole');
    const navigate = useNavigate();
    const [isLoggingOut, setIsLoggingOut] = useState(false);
    const [logoutError, setLogoutError] = useState('');

    const navItems = [
        { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, visible: true },
        { to: '/users', label: 'Users', icon: ShieldUser, visible: role === ADMIN_ROLE },
        { to: '/jobs', label: 'Jobs', icon: BriefcaseBusiness, visible: [HR_ROLE, ADMIN_ROLE, INTERVIEWER_ROLE].includes(role) },
        { to: '/candidates', label: 'Candidates', icon: Users, visible: role === HR_ROLE },
    ];

    const handleLogout = async () => {
        if (isLoggingOut) return;
        setLogoutError('');
        setIsLoggingOut(true);
        try {
            if (localStorage.getItem('basicAuth')) {
                await apiClient.post('/auth/logout');
            }
        } catch {
            setLogoutError('We could not sign you out right now. Please try again.');
            setIsLoggingOut(false);
            return;
        }
        clearAuthenticationData();
        navigate('/login', { replace: true });
        setIsLoggingOut(false);
    };

    return (
        <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
            <div className="sidebar-header">
                <div className="sidebar-brand">
                    {!isCollapsed ? (
                        <div>
                            <p className="sidebar-eyebrow">Interview Portal</p>
                            <h3 className="sidebar-title">TalentFlow</h3>
                        </div>
                    ) : null}
                </div>
                <button
                    type="button"
                    className="sidebar-toggle-btn"
                    onClick={() => setIsCollapsed(!isCollapsed)}
                    aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                >
                    {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
                </button>
            </div>

            <nav className="sidebar-nav" aria-label="Primary">
                {navItems.filter((item) => item.visible).map((item) => {
                    const Icon = item.icon;
                    return (
                        <NavLink key={item.to} to={item.to} className={({ isActive }) => `sidebar-nav-item ${isActive ? 'active' : ''}`}>
                            <Icon size={18} aria-hidden="true" />
                            {!isCollapsed ? <span>{item.label}</span> : null}
                        </NavLink>
                    );
                })}
            </nav>

            <div className="sidebar-footer">
                {logoutError ? <div className="sidebar-error">{logoutError}</div> : null}
                <button type="button" onClick={handleLogout} className="sidebar-logout-btn" disabled={isLoggingOut}>
                    <LogOut size={18} aria-hidden="true" />
                    {!isCollapsed ? <span>{isLoggingOut ? 'Logging out...' : 'Logout'}</span> : null}
                </button>
            </div>
        </aside>
    );
};

export default Sidebar;
