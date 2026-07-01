import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import UserForm from '../components/users/UserForm';
import { userService } from '../services/userService';
import {
    getUserManagementErrorMessage,
    isProtectedUser,
    validateUserForm,
} from '../utils/userManagement';
import '../styles/user-management.css';

/**
 * Render the administrator workflow for editing an existing user.
 *
 * @returns {JSX.Element} Edit user screen.
 */
const EditUserScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [role, setRole] = useState('');
    const [isActive, setIsActive] = useState(true);
    const [validationErrors, setValidationErrors] = useState({});
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        /**
         * Load the user data needed to prefill the edit form.
         */
        const fetchUser = async () => {
            try {
                setLoading(true);
                const userData = await userService.getUserById(id);
                setEmail(userData.email);
                setRole(userData.role);
                setIsActive(userData.is_active);
                setError(null);
            } catch (err) {
                setError(getUserManagementErrorMessage(err, 'Failed to load user data.'));
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, [id]);

    /**
     * Persist role changes for the selected user.
     *
     * @param {React.FormEvent<HTMLFormElement>} event - Form submission event.
     * @returns {Promise<void>}
     */
    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        const errors = validateUserForm({ email, role }, { emailReadonly: true });

        if (Object.keys(errors).length > 0) {
            setValidationErrors(errors);
            return;
        }

        try {
            setSaving(true);
            setValidationErrors({});
            await userService.updateUser(id, { role });
            navigate('/users', {
                replace: true,
                state: { successMessage: `User ${email} updated successfully.` },
            });
        } catch (err) {
            setError(getUserManagementErrorMessage(err, 'Failed to update user.'));
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return <div className="um-state">Loading user details...</div>;
    }

    const roleLocked = isProtectedUser({ email, is_active: isActive });
    const helperMessage = !isActive
        ? 'Disabled users cannot be reassigned until their account is re-enabled in the backend.'
        : email === 'admin@nucleusteq.com'
            ? 'The primary administrator role is protected from frontend edits.'
            : null;

    return (
        <div className="um-container um-form-page">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Administration</p>
                    <h1>Edit User</h1>
                    <p>Modify system access and role assignments.</p>
                </div>
            </div>

            <UserForm
                email={email}
                role={role}
                validationErrors={validationErrors}
                formError={error}
                helperMessage={helperMessage}
                emailDisabled
                roleDisabled={roleLocked}
                submitting={saving}
                submitLabel="Save Changes"
                submittingLabel="Saving..."
                onEmailChange={setEmail}
                onRoleChange={setRole}
                onCancel={() => navigate('/users')}
                onSubmit={handleSubmit}
            />
        </div>
    );
};

export default EditUserScreen;
