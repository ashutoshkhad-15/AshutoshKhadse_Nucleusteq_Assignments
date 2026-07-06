import { USER_ROLE_OPTIONS } from '../../utils/userManagement';

/**
 * Renders the user create and edit form.
 */
const UserForm = ({
    name,
    email,
    role,
    validationErrors,
    formError,
    helperMessage,
    nameDisabled,
    emailDisabled,
    roleDisabled,
    submitting,
    submitLabel,
    submittingLabel,
    onNameChange,
    onEmailChange,
    onRoleChange,
    onCancel,
    onSubmit,
}) => (
    <div className="form-card">
        {formError ? <div className="error-banner">{formError}</div> : null}
        <form onSubmit={onSubmit} noValidate>
            <h2 className="form-section-title">User Details</h2>
            <div className="form-grid">
                <div className="form-group form-group-full">
                    <label className="form-label" htmlFor="user-name">Full Name *</label>
                    <input
                        id="user-name"
                        type="text"
                        value={name}
                        onChange={(event) => onNameChange(event.target.value)}
                        disabled={submitting || nameDisabled}
                        className={`form-control ${validationErrors.name ? 'form-control-error' : ''}`}
                    />
                    {validationErrors.name ? <p className="field-error">{validationErrors.name}</p> : null}
                    {nameDisabled ? <p className="field-helper">The default administrator name cannot be changed.</p> : null}
                </div>
                <div className="form-group">
                    <label className="form-label" htmlFor="user-email">Employee Email *</label>
                    <input
                        id="user-email"
                        type="email"
                        value={email}
                        onChange={(event) => onEmailChange(event.target.value)}
                        disabled={emailDisabled}
                        className={`form-control ${validationErrors.email ? 'form-control-error' : ''}`}
                    />
                    {validationErrors.email ? <p className="field-error">{validationErrors.email}</p> : null}
                    {emailDisabled ? <p className="field-helper">Email addresses cannot be modified after account creation.</p> : null}
                </div>
                <div className="form-group">
                    <label className="form-label" htmlFor="user-role">System Role *</label>
                    <select
                        id="user-role"
                        value={role}
                        onChange={(event) => onRoleChange(event.target.value)}
                        disabled={roleDisabled}
                        className={`form-control ${validationErrors.role ? 'form-control-error' : ''}`}
                    >
                        <option value="">Select a role</option>
                        {USER_ROLE_OPTIONS.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
                    </select>
                    {validationErrors.role ? <p className="field-error">{validationErrors.role}</p> : null}
                    {helperMessage ? <p className="field-helper">{helperMessage}</p> : null}
                </div>
            </div>
            <div className="form-actions">
                <button type="button" onClick={onCancel} className="btn-secondary" disabled={submitting}>Cancel</button>
                <button type="submit" disabled={submitting || (emailDisabled && roleDisabled)} className="btn-primary">
                    {submitting ? submittingLabel : submitLabel}
                </button>
            </div>
        </form>
    </div>
);

export default UserForm;
