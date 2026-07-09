import { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { SIDEBAR_NAV_ITEMS } from '../../constants/sidebarNavigation';
import { signOut } from '../../utils/authSession';

const Sidebar = () => {
    const role = localStorage.getItem('userRole');
    const navigate = useNavigate();
    const [isLoggingOut, setIsLoggingOut] = useState(false);
    const [logoutError, setLogoutError] = useState('');

    const handleLogout = async () => {
        if (isLoggingOut) return;
        setLogoutError('');
        setIsLoggingOut(true);
        try {
            if (localStorage.getItem('basicAuth')) {
                await signOut();
            }
        } catch {
            setLogoutError('We could not sign you out right now. Please try again.');
            setIsLoggingOut(false);
            return;
        }
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
                {SIDEBAR_NAV_ITEMS.filter((item) => !item.visibleRoles || item.visibleRoles.includes(role)).map((item) => {
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
