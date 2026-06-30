import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthLayout from '../components/auth/AuthLayout';
import apiClient from '../services/apiService';

const LOGIN_TAGLINE = 'Streamline your recruitment process, schedule interviews, and track candidate progress all in one place.';

/**
 * Render the login form and establish a local Basic Auth session.
 *
 * @returns {JSX.Element} Login page.
 */
const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            setError('');

            if (!email.trim() || !password.trim()) {
                setError('Email or password is invalid.');
                return;
            }

            const response = await apiClient.post('/auth/login', { email, password });
            const userData = response.data.data;

            // First-time users must set a new password before entering the dashboard.
            if (userData.requires_password_reset) {
                navigate('/reset-password', { state: { email, old_password: password } });
                return;
            }

            // Persist authentication details for route guards and authenticated API calls.
            const token = btoa(`${email}:${password}`);
            localStorage.setItem('basicAuth', token);
            localStorage.setItem('userRole', userData.role);

            navigate('/dashboard');
        } catch {
            setError('Email or password is invalid.');
        }
    };

    return (
        <AuthLayout title="Interview Portal" tagline={LOGIN_TAGLINE}>
            <h2 className="auth-title">Welcome Back</h2>
            <p className="auth-subtitle">Please sign in to access your dashboard.</p>

            {error && <div className="error-text">{error}</div>}

            <form onSubmit={handleLogin} noValidate>
                <div className="form-group">
                    <input
                        type="email"
                        className="input-field"
                        placeholder="name@nucleusteq.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input
                        type="password"
                        className="input-field"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="submit" className="primary-btn">Sign In</button>
            </form>
        </AuthLayout>
    );
};

export default Login;
