import Sidebar from './Sidebar';

/**
 * Render the shared application shell around protected page content.
 *
 * @param {object} props - Component props.
 * @param {React.ReactNode} props.children - Page content displayed beside the sidebar.
 * @returns {JSX.Element} Layout with persistent navigation and content region.
 */
const MainLayout = ({ children }) => {
    return (
        <div className="sidebar-layout">
            <Sidebar />
            <div className="main-content">
                {children}
            </div>
        </div>
    );
};

export default MainLayout;
