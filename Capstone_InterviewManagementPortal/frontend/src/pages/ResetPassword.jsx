import { useState } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import AuthLayout from '../components/auth/AuthLayout';
import apiClient from '../services/apiService';

const RESET_PASSWORD_TAGLINE = 'As part of our standard security protocol, please establish a new, secure password for your account to access the Interview Portal.';

/**
 * Render the required password reset form for first-time login users.
 *
 * @returns {JSX.Element|null} Password reset page or login redirect.
 */
const ResetPassword = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { email, old_password } = location.state || {};

    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');

    if (!email) {
        return <Navigate to="/login" replace />;
    }

    const handleReset = async (e) => {
        e.preventDefault();
        setError('');

        // Match backend password rules before sending the reset request.
        if (!newPassword.trim() || !confirmPassword.trim()) {
            setError('Please fill out both password fields.');
            return;
        }
        if (newPassword.length < 6 || newPassword.length > 12) {
            setError('Password must be between 6 and 12 characters.');
            return;
        }
        if (newPassword !== confirmPassword) {
            setError('Passwords do not match. Please try again.');
            return;
        }

        try {
            await apiClient.post('/auth/reset-password', {
                email,
                old_password,
                new_password: newPassword,
            });

            alert('Password reset successfully. Please log in with your new password.');
            navigate('/login');
        } catch (err) {
            const serverError = err.response?.data?.details?.[0]?.msg || err.response?.data?.message;
            setError(serverError || 'Failed to reset password. Please try again.');
        }
    };

    return (
        <AuthLayout title="Security Update" tagline={RESET_PASSWORD_TAGLINE}>
            <h2 className="auth-title">Action Required</h2>
            <p className="auth-subtitle">Update the password for <strong>{email}</strong></p>

            {error && <div className="error-text">{error}</div>}

            <form onSubmit={handleReset} noValidate>
                <div className="form-group">
                    <input
                        type="password"
                        className="input-field"
                        placeholder="New Password (6-12 chars)"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                    />
                    <input
                        type="password"
                        className="input-field"
                        placeholder="Confirm New Password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                    />
                </div>
                <button type="submit" className="primary-btn">Secure My Account</button>
            </form>
        </AuthLayout>
    );
};

export default ResetPassword;
