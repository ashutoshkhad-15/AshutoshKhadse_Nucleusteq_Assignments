import { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import apiClient, { clearAuthenticationData } from '../../services/apiService';

const ADMIN_ROLE = 'ADMIN';
const HR_ROLE = 'HR';
const INTERVIEWER_ROLE = 'INTERVIEWER';

const Sidebar = () => {
    const role = localStorage.getItem('userRole');
    const navigate = useNavigate();
    const [isLoggingOut, setIsLoggingOut] = useState(false);
    const [logoutError, setLogoutError] = useState('');

    const navItems = [
        { to: '/dashboard', label: 'Dashboard', visible: true },
        { to: '/users', label: 'Users', visible: role === ADMIN_ROLE },
        { to: '/jobs', label: 'Jobs', visible: [HR_ROLE, ADMIN_ROLE, INTERVIEWER_ROLE].includes(role) },
        { to: '/candidates', label: 'Candidates', visible: role === HR_ROLE },
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
        <aside className="sidebar">
            <div className="sidebar-header">
                <div className="sidebar-brand">
                    <p className="sidebar-eyebrow">Interview Portal</p>
                    <h3 className="sidebar-title">TalentFlow</h3>
                </div>
            </div>

            <nav className="sidebar-nav" aria-label="Primary">
                {navItems.filter((item) => item.visible).map((item) => {
                    return (
                        <NavLink key={item.to} to={item.to} className={({ isActive }) => `sidebar-nav-item ${isActive ? 'active' : ''}`}>
                            <span>{item.label}</span>
                        </NavLink>
                    );
                })}
            </nav>

            <div className="sidebar-footer">
                {logoutError ? <div className="sidebar-error">{logoutError}</div> : null}
                <button type="button" onClick={handleLogout} className="sidebar-logout-btn" disabled={isLoggingOut}>
                    <span>{isLoggingOut ? 'Logging out...' : 'Logout'}</span>
                </button>
            </div>
        </aside>
    );
};

export default Sidebar;
