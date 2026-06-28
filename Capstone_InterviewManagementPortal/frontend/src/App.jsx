import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import Login from './pages/Login';
import ResetPassword from './pages/ResetPassword';
import AdminRoute from './components/routing/AdminRoute';
import CreateUserScreen from './pages/CreateUserScreen';
import EditUserScreen from './pages/EditUserScreen';
import UserListScreen from './pages/UserListScreen';

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
                <Route element={<AdminRoute />}>
                    <Route path="/users" element={<UserListScreen />} />
                    <Route path="/users/create" element={<CreateUserScreen />} />
                    <Route path="/users/edit/:id" element={<EditUserScreen />} />
                </Route>
                <Route path="*" element={<NotFound />} />
            </Routes>
        </Router>
    );
}

export default App;
