const PASSWORD_MIN_LENGTH = 6;
const PASSWORD_MAX_LENGTH = 12;

/**
 * Validate the password reset form before submitting it to the backend.
 *
 * @param {string} newPassword - Proposed replacement password.
 * @param {string} confirmPassword - Confirmation password.
 * @returns {string} Validation error message or an empty string when valid.
 */
export const validatePasswordReset = (newPassword, confirmPassword) => {
    if (!newPassword.trim() || !confirmPassword.trim()) {
        return 'Please fill out both password fields.';
    }

    if (newPassword.length < PASSWORD_MIN_LENGTH || newPassword.length > PASSWORD_MAX_LENGTH) {
        return `Password must be between ${PASSWORD_MIN_LENGTH} and ${PASSWORD_MAX_LENGTH} characters.`;
    }

    if (newPassword !== confirmPassword) {
        return 'Passwords do not match. Please try again.';
    }

    return '';
};

/**
 * Extract a user-facing error message from an API failure.
 *
 * @param {unknown} error - Error returned by the request layer.
 * @param {string} fallbackMessage - Message to use when the server is silent.
 * @returns {string} Normalized error message.
 */
export const getAuthErrorMessage = (error, fallbackMessage) => {
    return error?.response?.data?.details?.[0]?.msg || error?.response?.data?.message || fallbackMessage;
};
