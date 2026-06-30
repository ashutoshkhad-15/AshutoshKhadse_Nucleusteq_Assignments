import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import UserForm from '../components/users/UserForm';
import { userService } from '../services/userService';
import { getUserManagementErrorMessage, validateUserForm } from '../utils/userManagement';
import '../styles/user-management.css';

/**
 * Render the administrator workflow for creating a new user account.
 *
 * @returns {JSX.Element} Create user screen.
 */
const CreateUserScreen = () => {
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [role, setRole] = useState('');
    const [validationErrors, setValidationErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    /**
     * Create a user after client-side validation passes.
     *
     * @param {React.FormEvent<HTMLFormElement>} event - Form submission event.
     * @returns {Promise<void>}
     */
    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        const trimmedEmail = email.trim();
        const errors = validateUserForm({ email: trimmedEmail, role });

        if (Object.keys(errors).length > 0) {
            setValidationErrors(errors);
            return;
        }

        try {
            setLoading(true);
            setValidationErrors({});
            await userService.createUser({ email: trimmedEmail, role });
            navigate('/users', {
                replace: true,
                state: { successMessage: `User ${trimmedEmail} created successfully.` },
            });
        } catch (err) {
            setError(getUserManagementErrorMessage(err, 'Failed to create user. Please try again.'));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="um-container um-form-page">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Administration</p>
                    <h1>Create User</h1>
                    <p>Provision a new employee account. A temporary password will be generated automatically.</p>
                </div>
            </div>

            <UserForm
                email={email}
                role={role}
                validationErrors={validationErrors}
                formError={error}
                emailDisabled={false}
                roleDisabled={false}
                submitting={loading}
                submitLabel="Create User"
                submittingLabel="Creating..."
                onEmailChange={setEmail}
                onRoleChange={setRole}
                onCancel={() => navigate('/users')}
                onSubmit={handleSubmit}
            />
        </div>
    );
};

export default CreateUserScreen;
