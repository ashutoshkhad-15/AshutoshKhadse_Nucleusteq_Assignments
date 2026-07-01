import { USER_ROLE_OPTIONS } from '../../utils/userManagement';

/**
 * Render the shared create/edit user form fields and actions.
 *
 * @param {object} props - Component props.
 * @param {string} props.email - Current email value.
 * @param {string} props.role - Current role value.
 * @param {{ email?: string, role?: string }} props.validationErrors - Field validation errors.
 * @param {string | null} props.formError - Form-level error message.
 * @param {string | null} props.helperMessage - Optional guidance shown beneath the form.
 * @param {boolean} props.emailDisabled - Whether the email field is read-only.
 * @param {boolean} props.roleDisabled - Whether the role field is read-only.
 * @param {boolean} props.submitting - Whether the form is being submitted.
 * @param {string} props.submitLabel - Idle submit button label.
 * @param {string} props.submittingLabel - Busy submit button label.
 * @param {(value: string) => void} props.onEmailChange - Email update callback.
 * @param {(value: string) => void} props.onRoleChange - Role update callback.
 * @param {() => void} props.onCancel - Cancel action.
 * @param {(event: React.FormEvent<HTMLFormElement>) => void} props.onSubmit - Submit handler.
 * @returns {JSX.Element} Shared user form UI.
 */
const UserForm = ({
    email,
    role,
    validationErrors,
    formError,
    helperMessage,
    emailDisabled,
    roleDisabled,
    submitting,
    submitLabel,
    submittingLabel,
    onEmailChange,
    onRoleChange,
    onCancel,
    onSubmit,
}) => (
    <div className="form-card">
        {formError ? <div className="error-banner">{formError}</div> : null}

        <form onSubmit={onSubmit} noValidate>
            <div className="form-section">
                <div className="form-section-header">
                    <h2 className="form-section-title">User Details</h2>
                </div>

                <div className="form-grid">
                    <div className="form-group">
                        <label className="form-label" htmlFor="user-email">
                            Employee Email <span className="required-indicator">*</span>
                        </label>
                        <input
                            id="user-email"
                            type="email"
                            value={email}
                            onChange={(event) => onEmailChange(event.target.value)}
                            disabled={emailDisabled}
                            className={`form-control ${validationErrors.email ? 'form-control-error' : ''}`}
                            placeholder="firstname.lastname@nucleusteq.com"
                            aria-invalid={Boolean(validationErrors.email)}
                            aria-describedby={validationErrors.email ? 'user-email-error' : undefined}
                        />
                        {validationErrors.email ? (
                            <p id="user-email-error" className="field-error">
                                {validationErrors.email}
                            </p>
                        ) : null}
                        {emailDisabled ? (
                            <p className="field-helper">Email addresses cannot be modified after account creation.</p>
                        ) : null}
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="user-role">
                            System Role <span className="required-indicator">*</span>
                        </label>
                        <select
                            id="user-role"
                            value={role}
                            onChange={(event) => onRoleChange(event.target.value)}
                            disabled={roleDisabled}
                            className={`form-control ${validationErrors.role ? 'form-control-error' : ''}`}
                            aria-invalid={Boolean(validationErrors.role)}
                            aria-describedby={validationErrors.role ? 'user-role-error' : undefined}
                        >
                            <option value="">Select a role</option>
                            {USER_ROLE_OPTIONS.map((option) => (
                                <option key={option.value} value={option.value}>
                                    {option.label}
                                </option>
                            ))}
                        </select>
                        {validationErrors.role ? (
                            <p id="user-role-error" className="field-error">
                                {validationErrors.role}
                            </p>
                        ) : null}
                        {helperMessage ? <p className="field-helper">{helperMessage}</p> : null}
                    </div>
                </div>
            </div>

            <div className="form-actions">
                <button
                    type="button"
                    onClick={onCancel}
                    className="btn-secondary"
                    disabled={submitting}
                >
                    Cancel
                </button>
                <button type="submit" disabled={submitting || roleDisabled} className="btn-primary">
                    {submitting ? submittingLabel : submitLabel}
                </button>
            </div>
        </form>
    </div>
);

export default UserForm;
