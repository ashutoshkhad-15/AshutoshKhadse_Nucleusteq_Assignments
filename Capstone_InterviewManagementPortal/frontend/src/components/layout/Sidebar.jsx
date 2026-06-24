import { NavLink } from 'react-router-dom';

/**
 * Render role-aware navigation links for protected application pages.
 *
 * The current role is read from local storage until a centralized auth context
 * is introduced. Link visibility mirrors the backend authorization model so
 * users only see sections relevant to their role.
 *
 * @returns {JSX.Element} Sidebar navigation.
 */
const Sidebar = () => {
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

/**
 * Inline styles used by the early layout scaffold.
 *
 * Centralizing these values keeps component markup readable until a shared
 * design system or stylesheet owns layout styling.
 */
const styles = {
    sidebar: { width: '250px', background: '#f4f4f4', height: '100vh', padding: '20px', borderRight: '1px solid #ddd' },
    title: { color: '#333', marginBottom: '30px' },
    navList: { listStyle: 'none', padding: 0 },
    link: { textDecoration: 'none', color: '#0056b3', display: 'block', padding: '10px 0' }
};

export default Sidebar;
