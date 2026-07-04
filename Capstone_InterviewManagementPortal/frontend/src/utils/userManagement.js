export const USER_ROLE_OPTIONS = [
    { value: 'ADMIN', label: 'Admin' },
    { value: 'HR', label: 'HR' },
    { value: 'INTERVIEWER', label: 'Interviewer' },
];

export const DEFAULT_ADMIN_EMAIL = 'admin@nucleusteq.com';

const ALLOWED_ROLES = new Set(USER_ROLE_OPTIONS.map((option) => option.value));
const NUCLEUSTEQ_EMAIL_PATTERN = /^[A-Za-z0-9._%+-]+@nucleusteq\.com$/i;

const normalizeText = (value) => value?.trim() || '';

/**
 * Validate a user name using the shared user-management rules.
 *
 * @param {string} name - Raw name value.
 * @returns {string} Normalized name value or an empty string when invalid.
 */
export const validateUserName = (name) => {
    const normalizedName = normalizeText(name);

    if (!normalizedName) {
        throw new Error('Name is required.');
    }

    if (normalizedName.length < 2 || normalizedName.length > 100) {
        throw new Error('Name must be between 2 and 100 characters.');
    }

    return normalizedName;
};

/**
 * Validate a corporate email address using the shared user-management rules.
 *
 * @param {string} email - Raw email value.
 * @returns {string} Normalized email value.
 */
export const validateUserEmail = (email) => {
    const normalizedEmail = normalizeText(email).toLowerCase();

    if (!normalizedEmail) {
        throw new Error('Email is required.');
    }

    if (!NUCLEUSTEQ_EMAIL_PATTERN.test(normalizedEmail)) {
        throw new Error('Enter a valid @nucleusteq.com email address.');
    }

    return normalizedEmail;
};

/**
 * Validate the user management form before an API request is sent.
 *
 * @param {{ name?: string, email?: string, role?: string }} values - Form values to validate.
 * @returns {{ email?: string, role?: string }} Field-level validation errors.
 */
export const validateUserForm = (values) => {
    const errors = {};
    const normalizedName = normalizeText(values.name);
    const normalizedEmail = normalizeText(values.email).toLowerCase();

    if (!normalizedName) {
        errors.name = 'Name is required.';
    } else if (normalizedName.length < 2 || normalizedName.length > 100) {
        errors.name = 'Name must be between 2 and 100 characters.';
    }

    if (!normalizedEmail) {
        errors.email = 'Email is required.';
    } else if (!NUCLEUSTEQ_EMAIL_PATTERN.test(normalizedEmail)) {
        errors.email = 'Enter a valid @nucleusteq.com email address.';
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
    return error?.response?.data?.details?.[0]?.msg || error?.response?.data?.message || fallbackMessage;
};

/**
 * Check whether the current user should be protected from admin edits.
 *
 * @param {{ email?: string, is_active?: boolean }} user - User record.
 * @returns {boolean} Whether editing actions should be restricted.
 */
export const isProtectedUser = (user) => user?.email === DEFAULT_ADMIN_EMAIL || user?.is_active === false;

/**
 * Format the visible row range shown in the pagination footer.
 *
 * @param {number} page - Current page number.
 * @param {number} limit - Items per page.
 * @param {number} itemCount - Number of rows on the current page.
 * @returns {string} Human-readable range label.
 */
export const formatUserRange = (page, limit, itemCount) => {
    if (!itemCount) {
        return '0 to 0';
    }

    const startIndex = (page - 1) * limit + 1;
    return `${startIndex} to ${startIndex + itemCount - 1}`;
};
