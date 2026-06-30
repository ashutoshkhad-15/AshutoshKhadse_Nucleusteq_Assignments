import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';

/**
 * Placeholder login screen used until the authentication page is implemented.
 *
 * @returns {JSX.Element} Login route content.
 */
const Login = () => <h2>Login Page</h2>;

/**
 * Placeholder dashboard screen used as the authenticated landing page.
 *
 * @returns {JSX.Element} Dashboard route content.
 */
const Dashboard = () => <h2>Dashboard Placeholder</h2>;

/**
 * Fallback screen rendered for unmatched routes.
 *
 * @returns {JSX.Element} Not-found route content.
 */
const NotFound = () => <h2>404 - Page Not Found</h2>;

/**
 * Configure client-side routes for the Interview Management Portal.
 *
 * Public routes are rendered directly. Authenticated application routes are
 * wrapped by the shared layout so navigation remains consistent across pages.
 *
 * @returns {JSX.Element} Application router tree.
 */
function App() {
    return (
        <Router>
            <Routes>
                {/* Keep login outside the protected layout so authentication can use a focused screen. */}
                <Route path="/login" element={<Login />} />
                
                <Route path="/" element={<Navigate to="/dashboard" />} />
                <Route path="/dashboard" element={<MainLayout><Dashboard /></MainLayout>} />
                
                <Route path="*" element={<NotFound />} />
            </Routes>
        </Router>
    );
}

export default App;
