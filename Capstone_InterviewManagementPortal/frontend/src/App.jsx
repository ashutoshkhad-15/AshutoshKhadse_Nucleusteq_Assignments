import { BrowserRouter as Router, Navigate, Route, Routes } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import Login from './pages/Login';
import ResetPassword from './pages/ResetPassword';

const Dashboard = () => <h2>Dashboard Placeholder</h2>;
const NotFound = () => <h2>404 - Page Not Found</h2>;

/**
 * Protects pages that require an authenticated browser session.
 *
 * @param {object} props - Component props.
 * @param {React.ReactNode} props.children - Protected page content.
 * @returns {JSX.Element} Protected content or login redirect.
 */
const ProtectedRoute = ({ children }) => {
    const isAuthenticated = !!localStorage.getItem('basicAuth');

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    return children;
};

/**
 * Keeps authenticated users out of public authentication pages.
 *
 * @param {object} props - Component props.
 * @param {React.ReactNode} props.children - Public page content.
 * @returns {JSX.Element} Public content or dashboard redirect.
 */
const PublicRoute = ({ children }) => {
    const isAuthenticated = !!localStorage.getItem('basicAuth');

    if (isAuthenticated) {
        return <Navigate to="/dashboard" replace />;
    }

    return children;
};

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Navigate to="/dashboard" />} />
                <Route
                    path="/login"
                    element={(
                        <PublicRoute>
                            <Login />
                        </PublicRoute>
                    )}
                />
                <Route
                    path="/reset-password"
                    element={(
                        <PublicRoute>
                            <ResetPassword />
                        </PublicRoute>
                    )}
                />
                <Route
                    path="/dashboard"
                    element={(
                        <ProtectedRoute>
                            <MainLayout>
                                <Dashboard />
                            </MainLayout>
                        </ProtectedRoute>
                    )}
                />
                <Route path="*" element={<NotFound />} />
            </Routes>
        </Router>
    );
}

export default App;
