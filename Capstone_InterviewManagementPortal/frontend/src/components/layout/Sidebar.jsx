import { NavLink } from 'react-router-dom';

const Sidebar = () => {
    // In a real app, role will dictate which links are visible
    const role = localStorage.getItem('userRole');

    return (
        <div style={styles.sidebar}>
            <h3 style={styles.title}>Interview Portal</h3>
            <ul style={styles.navList}>
                <li><NavLink to="/dashboard" style={styles.link}>Dashboard</NavLink></li>
                {(role === 'ADMIN' || role === 'HR') && (
                    <li><NavLink to="/users" style={styles.link}>Users</NavLink></li>
                )}
                {(role === 'HR') && (
                    <>
                        <li><NavLink to="/jobs" style={styles.link}>Jobs</NavLink></li>
                        <li><NavLink to="/candidates" style={styles.link}>Candidates</NavLink></li>
                    </>
                )}
                {(role === 'HR' || role === 'INTERVIEWER') && (
                    <li><NavLink to="/interviews" style={styles.link}>Interviews</NavLink></li>
                )}
            </ul>
        </div>
    );
};

const styles = {
    sidebar: { width: '250px', background: '#f4f4f4', height: '100vh', padding: '20px', borderRight: '1px solid #ddd' },
    title: { color: '#333', marginBottom: '30px' },
    navList: { listStyle: 'none', padding: 0 },
    link: { textDecoration: 'none', color: '#0056b3', display: 'block', padding: '10px 0' }
};

export default Sidebar;