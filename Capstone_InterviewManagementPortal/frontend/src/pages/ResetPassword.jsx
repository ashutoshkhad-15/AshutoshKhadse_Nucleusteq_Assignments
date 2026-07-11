import { useState } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import AuthLayout from '../components/auth/AuthLayout';
import PasswordField from '../components/auth/PasswordField';
import apiClient from '../services/apiService';
import { getAuthErrorMessage, validatePasswordReset } from '../utils/auth';

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
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [showNewPassword, setShowNewPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    if (!email) {
        return <Navigate to="/login" replace />;
    }

    const handleReset = async (e) => {
        e.preventDefault();

        if (isSubmitting) {
            return;
        }

        setError('');
        setIsSubmitting(true);

        const validationError = validatePasswordReset(newPassword, confirmPassword);
        if (validationError) {
            setError(validationError);
            setIsSubmitting(false);
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
            setError(getAuthErrorMessage(err, 'Failed to reset password. Please try again.'));
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <AuthLayout title="Security Update" tagline={RESET_PASSWORD_TAGLINE}>
            <h2 className="auth-title">Action Required</h2>
            <p className="auth-subtitle">Update the password for <strong>{email}</strong></p>

            {error && <div className="error-text">{error}</div>}

            <form onSubmit={handleReset} noValidate aria-busy={isSubmitting}>
                <label className="field-label" htmlFor="new-password">New password</label>
                <PasswordField
                    id="new-password"
                    value={newPassword}
                    onChange={setNewPassword}
                    placeholder="New Password (6-12 chars)"
                    visible={showNewPassword}
                    onToggleVisibility={() => setShowNewPassword((value) => !value)}
                    disabled={isSubmitting}
                    toggleLabel={showNewPassword ? 'Hide new password' : 'Show new password'}
                />
                <label className="field-label" htmlFor="confirm-password">Confirm password</label>
                <PasswordField
                    id="confirm-password"
                    value={confirmPassword}
                    onChange={setConfirmPassword}
                    placeholder="Confirm New Password"
                    visible={showConfirmPassword}
                    onToggleVisibility={() => setShowConfirmPassword((value) => !value)}
                    disabled={isSubmitting}
                    toggleLabel={showConfirmPassword ? 'Hide confirm password' : 'Show confirm password'}
                />
                <button type="submit" className="primary-btn" disabled={isSubmitting}>
                    {isSubmitting ? 'Resetting Password...' : 'Secure My Account'}
                </button>
            </form>
        </AuthLayout>
    );
};

export default ResetPassword;
