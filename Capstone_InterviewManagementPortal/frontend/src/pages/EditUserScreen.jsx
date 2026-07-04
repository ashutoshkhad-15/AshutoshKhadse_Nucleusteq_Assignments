import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import UserForm from '../components/users/UserForm';
import { userService } from '../services/userService';
import '../styles/user-management.css';
import {
    DEFAULT_ADMIN_EMAIL,
    getUserManagementErrorMessage,
    isProtectedUser,
    validateUserForm,
} from '../utils/userManagement';

/**
 * Render the administrator workflow for editing an existing user.
 *
 * @returns {JSX.Element} Edit user screen.
 */
const EditUserScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [role, setRole] = useState('');
    const [isActive, setIsActive] = useState(true);
    const [validationErrors, setValidationErrors] = useState({});
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);

    const isDefaultAdmin = email === DEFAULT_ADMIN_EMAIL;
    const emailLocked = isProtectedUser({ email, is_active: isActive });
    const nameLocked = isDefaultAdmin;
    const roleLocked = emailLocked;

    useEffect(() => {
        /**
         * Load the user data needed to prefill the edit form.
         * We schedule the request after a short delay so React StrictMode
         * can mount/unmount the component once without issuing duplicate fetches.
         */
        const controller = new AbortController();
        const timeoutId = window.setTimeout(async () => {
            try {
                setLoading(true);
                const userData = await userService.getUserById(id, { signal: controller.signal });
                setName(userData.name || '');
                setEmail(userData.email);
                setRole(userData.role);
                setIsActive(userData.is_active);
                setError(null);
            } catch (err) {
                if (err?.name === 'CanceledError') {
                    return;
                }
                setError(getUserManagementErrorMessage(err, 'Failed to load user data.'));
            } finally {
                setLoading(false);
            }
        }, 20);

        return () => {
            window.clearTimeout(timeoutId);
            controller.abort();
        };
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
        const errors = validateUserForm({ name, email, role }, { emailReadonly: emailLocked });

        if (Object.keys(errors).length > 0) {
            setValidationErrors(errors);
            return;
        }

        try {
            setSaving(true);
            setValidationErrors({});
            const payload = {};
            if (!nameLocked) {
                payload.name = name.trim();
            }

            if (!emailLocked) {
                payload.email = email.trim();
            }

            if (!roleLocked) {
                payload.role = role;
            }

            await userService.updateUser(id, payload);
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

    const helperMessage = isDefaultAdmin
        ? 'The default administrator account is locked to preserve system access.'
        : !isActive
            ? 'Disabled users cannot be reassigned until their account is re-enabled in the backend.'
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
                name={name}
                email={email}
                role={role}
                validationErrors={validationErrors}
                formError={error}
                helperMessage={helperMessage}
                nameDisabled={nameLocked}
                emailDisabled={emailLocked}
                roleDisabled={roleLocked}
                submitting={saving}
                submitLabel="Save Changes"
                submittingLabel="Saving..."
                onNameChange={setName}
                onEmailChange={setEmail}
                onRoleChange={setRole}
                onCancel={() => navigate('/users')}
                onSubmit={handleSubmit}
            />
        </div>
    );
};

export default EditUserScreen;
