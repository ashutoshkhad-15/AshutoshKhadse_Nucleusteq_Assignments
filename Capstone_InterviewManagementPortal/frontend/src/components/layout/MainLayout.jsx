import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

/**
 * Render the shared application shell around protected page content.
 *
 * @param {object} props - Component props.
 * @param {React.ReactNode} props.children - Page content displayed beside the sidebar.
 * @returns {JSX.Element} Layout with persistent navigation and content region.
 */
const MainLayout = ({ children }) => {
    const [isCollapsed, setIsCollapsed] = useState(false);

    return (
        <div className="sidebar-layout">
            <Sidebar isCollapsed={isCollapsed} setIsCollapsed={setIsCollapsed} />

            <div className={`main-content ${isCollapsed ? 'content-expanded' : ''}`}>
                {children || <Outlet />}
            </div>
        </div>
    );
};

export default MainLayout;
