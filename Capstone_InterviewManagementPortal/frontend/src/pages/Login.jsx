import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthLayout from '../components/auth/AuthLayout';
import PasswordField from '../components/auth/PasswordField';
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
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();

        if (isSubmitting) {
            return;
        }

        setError('');
        setIsSubmitting(true);

        try {
            if (!email.trim() || !password.trim()) {
                setError('Email or password is invalid.');
                return;
            }

            const response = await apiClient.post('/auth/login', { email, password });
            const userData = response.data.data;

            if (userData.requires_password_reset) {
                navigate('/reset-password', { state: { email, old_password: password } });
                return;
            }

            const token = btoa(`${email}:${password}`);
            localStorage.setItem('basicAuth', token);
            localStorage.setItem('userRole', userData.role);

            navigate('/dashboard');
        } catch {
            setError('Email or password is invalid.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <AuthLayout title="Interview Portal" tagline={LOGIN_TAGLINE}>
            <h2 className="auth-title">Welcome Back</h2>
            <p className="auth-subtitle">Please sign in to access your dashboard.</p>

            {error && <div className="error-text">{error}</div>}

            <form onSubmit={handleLogin} noValidate aria-busy={isSubmitting}>
                <label className="field-label" htmlFor="login-email">Email</label>
                <input
                    id="login-email"
                    type="email"
                    className="input-field"
                    placeholder="name@nucleusteq.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    disabled={isSubmitting}
                />

                <label className="field-label" htmlFor="login-password">Password</label>
                <PasswordField
                    id="login-password"
                    value={password}
                    onChange={setPassword}
                    placeholder="Password"
                    visible={showPassword}
                    onToggleVisibility={() => setShowPassword((value) => !value)}
                    disabled={isSubmitting}
                    toggleLabel={showPassword ? 'Hide password' : 'Show password'}
                />
                <button type="submit" className="primary-btn" disabled={isSubmitting}>
                    {isSubmitting ? 'Signing in...' : 'Sign In'}
                </button>
            </form>
        </AuthLayout>
    );
};

export default Login;
