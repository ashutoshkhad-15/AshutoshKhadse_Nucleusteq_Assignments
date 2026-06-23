import Sidebar from './Sidebar';

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