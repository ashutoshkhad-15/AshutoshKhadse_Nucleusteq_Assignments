import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';

// Placeholder Pages for routing setup
const Login = () => <h2>Login Page</h2>;
const Dashboard = () => <h2>Dashboard Placeholder</h2>;
const NotFound = () => <h2>404 - Page Not Found</h2>;

function App() {
    return (
        <Router>
            <Routes>
                {/* Public Route */}
                <Route path="/login" element={<Login />} />
                
                {/* Protected Routes Wrapper */}
                <Route path="/" element={<Navigate to="/dashboard" />} />
                <Route path="/dashboard" element={<MainLayout><Dashboard /></MainLayout>} />
                
                {/* Fallback */}
                <Route path="*" element={<NotFound />} />
            </Routes>
        </Router>
    );
}

export default App;