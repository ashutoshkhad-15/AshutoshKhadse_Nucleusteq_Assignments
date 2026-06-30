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
        <div style={{ display: 'flex', minHeight: '100vh', margin: 0 }}>
            <Sidebar />
            <div style={{ flex: 1, padding: '20px' }}>
                {children}
            </div>
        </div>
    );
};

export default MainLayout;
