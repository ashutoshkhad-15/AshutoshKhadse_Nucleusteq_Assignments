export const USER_ROLE_OPTIONS = [
    { value: 'ADMIN', label: 'Admin' },
    { value: 'HR', label: 'HR' },
    { value: 'INTERVIEWER', label: 'Interviewer' },
];

const ALLOWED_ROLES = new Set(USER_ROLE_OPTIONS.map((option) => option.value));
const NUCLEUSTEQ_EMAIL_PATTERN = /^[A-Za-z0-9._%+-]+@nucleusteq\.com$/i;

/**
 * Validate the user management form before an API request is sent.
 *
 * @param {{ email?: string, role?: string }} values - Form values to validate.
 * @param {{ emailReadonly?: boolean }} [options] - Validation options for edit mode.
 * @returns {{ email?: string, role?: string }} Field-level validation errors.
 */
export const validateUserForm = (values, options = {}) => {
    const errors = {};
    const normalizedEmail = values.email?.trim() || '';

    if (!options.emailReadonly) {
        if (!normalizedEmail) {
            errors.email = 'Email is required.';
        } else if (!NUCLEUSTEQ_EMAIL_PATTERN.test(normalizedEmail)) {
            errors.email = 'Enter a valid @nucleusteq.com email address.';
        }
    }

    if (!values.role) {
        errors.role = 'Role is required.';
    } else if (!ALLOWED_ROLES.has(values.role)) {
        errors.role = 'Select a valid role.';
    }

    return errors;
};

/**
 * Normalize API failures into a single message for user-facing feedback.
 *
 * @param {unknown} error - Error thrown by the request layer.
 * @param {string} fallbackMessage - Message used when the server does not supply one.
 * @returns {string} Human-readable error text.
 */
export const getUserManagementErrorMessage = (error, fallbackMessage) => {
    const apiMessage = error?.response?.data?.details?.[0]?.msg || error?.response?.data?.message;
    return apiMessage || fallbackMessage;
};

/**
 * Check whether the current user should be protected from admin edits.
 *
 * @param {{ email?: string, is_active?: boolean }} user - User record.
 * @returns {boolean} Whether editing actions should be restricted.
 */
export const isProtectedUser = (user) => user?.email === 'admin@nucleusteq.com' || user?.is_active === false;
