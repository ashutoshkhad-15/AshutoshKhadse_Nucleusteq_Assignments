import { useEffect, useMemo, useState } from 'react';

export const JOB_STATUS_OPTIONS = [
    { value: 'ALL', label: 'All status' },
    { value: 'ACTIVE', label: 'Open roles' },
    { value: 'INACTIVE', label: 'Closed roles' },
];

export const JOB_FORM_DEFAULTS = {
    title: '',
    department: '',
    description: '',
    skills: '',
    experience_required: '',
    location: '',
};

const JOB_FIELD_LIMITS = {
    title: { min: 3, max: 100 },
    department: { min: 2, max: 50 },
    description: { min: 10, max: 3000 },
    experience_required: { min: 2, max: 60 },
    location: { min: 2, max: 80 },
};

export const JOB_LIST_BREAKPOINT = 900;
export const JOB_LIST_SKELETON_COUNT = 6;
export const JOB_SEARCH_DEBOUNCE_MS = 1000;

/**
 * Parse the freeform skills field into a trimmed unique array.
 *
 * @param {string} skillsInput - Comma or newline separated skills.
 * @returns {Array<string>} Normalized skills array.
 */
export const normalizeSkills = (skillsInput = '') => (
    [...new Set(
        skillsInput
            .split(/[\n,]/)
            .map((skill) => skill.trim())
            .filter(Boolean)
    )]
);

/**
 * Convert API job data into form-friendly values.
 *
 * @param {object} job - Job payload from the backend.
 * @returns {object} Form-ready values.
 */
export const mapJobToFormValues = (job = {}) => ({
    title: job.title || '',
    department: job.department || '',
    description: job.description || '',
    skills: Array.isArray(job.skills) ? job.skills.join(', ') : '',
    experience_required: job.experience_required || '',
    location: job.location || '',
});

/**
 * Prepare validated form values for create and update requests.
 *
 * @param {object} values - Raw form values.
 * @returns {object} API-ready payload.
 */
export const buildJobPayload = (values) => ({
    title: values.title.trim(),
    department: values.department.trim(),
    description: values.description.trim(),
    skills: normalizeSkills(values.skills),
    experience_required: values.experience_required.trim(),
    location: values.location.trim(),
});

/**
 * Validate the job form before an API request is sent.
 *
 * @param {object} values - Form values to validate.
 * @returns {object} Field-level validation errors.
 */
export const validateJobForm = (values) => {
    const errors = {};
    const payload = buildJobPayload(values);

    if (!payload.title) {
        errors.title = 'Job title is required.';
    } else if (payload.title.length < JOB_FIELD_LIMITS.title.min || payload.title.length > JOB_FIELD_LIMITS.title.max) {
        errors.title = `Job title must be between ${JOB_FIELD_LIMITS.title.min} and ${JOB_FIELD_LIMITS.title.max} characters.`;
    }

    if (!payload.department) {
        errors.department = 'Department is required.';
    } else if (
        payload.department.length < JOB_FIELD_LIMITS.department.min
        || payload.department.length > JOB_FIELD_LIMITS.department.max
    ) {
        errors.department = `Department must be between ${JOB_FIELD_LIMITS.department.min} and ${JOB_FIELD_LIMITS.department.max} characters.`;
    }

    if (!payload.description) {
        errors.description = 'Job description is required.';
    } else if (
        payload.description.length < JOB_FIELD_LIMITS.description.min
        || payload.description.length > JOB_FIELD_LIMITS.description.max
    ) {
        errors.description = `Description must be between ${JOB_FIELD_LIMITS.description.min} and ${JOB_FIELD_LIMITS.description.max} characters.`;
    }

    if (payload.skills.length === 0) {
        errors.skills = 'Add at least one required skill.';
    }

    if (!payload.experience_required) {
        errors.experience_required = 'Experience requirement is required.';
    } else if (
        payload.experience_required.length < JOB_FIELD_LIMITS.experience_required.min
        || payload.experience_required.length > JOB_FIELD_LIMITS.experience_required.max
    ) {
        errors.experience_required = `Experience requirement must be between ${JOB_FIELD_LIMITS.experience_required.min} and ${JOB_FIELD_LIMITS.experience_required.max} characters.`;
    }

    if (!payload.location) {
        errors.location = 'Location is required.';
    } else if (
        payload.location.length < JOB_FIELD_LIMITS.location.min
        || payload.location.length > JOB_FIELD_LIMITS.location.max
    ) {
        errors.location = `Location must be between ${JOB_FIELD_LIMITS.location.min} and ${JOB_FIELD_LIMITS.location.max} characters.`;
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
export const getJobManagementErrorMessage = (error, fallbackMessage) => {
    const detailsMessage = error?.response?.data?.details?.[0]?.msg;
    const apiMessage = error?.response?.data?.message;
    return detailsMessage || apiMessage || fallbackMessage;
};

/**
 * Return a viewport-aware page size for job cards.
 *
 * @param {number} viewportWidth - Current viewport width.
 * @returns {number} Items per page.
 */
export const getJobItemsPerPage = (viewportWidth) => (viewportWidth < JOB_LIST_BREAKPOINT ? 6 : 8);

/**
 * Filter jobs for the listing screen.
 *
 * @param {Array<object>} jobs - Available jobs.
 * @param {string} searchTerm - Debounced search input.
 * @param {string} statusFilter - Active status filter.
 * @returns {Array<object>} Visible jobs.
 */
export const filterJobs = (jobs, searchTerm, statusFilter) => {
    const normalizedQuery = searchTerm.trim().toLowerCase();

    return jobs.filter((job) => {
        const searchableText = [
            job.title,
            job.department,
            job.location,
            job.experience_required,
            ...(Array.isArray(job.skills) ? job.skills : []),
        ]
            .filter(Boolean)
            .join(' ')
            .toLowerCase();

        const matchesSearch = !normalizedQuery || searchableText.includes(normalizedQuery);
        const matchesStatus = statusFilter === 'ALL'
            || (statusFilter === 'ACTIVE' && job.is_active)
            || (statusFilter === 'INACTIVE' && !job.is_active);

        return matchesSearch && matchesStatus;
    });
};

/**
 * Create a throttled function wrapper.
 *
 * @template {(...args: Array<any>) => void} T
 * @param {T} callback - Function to throttle.
 * @param {number} wait - Minimum time between calls in milliseconds.
 * @returns {T} Throttled callback.
 */
export const throttle = (callback, wait) => {
    let lastCallTime = 0;
    let timeoutId = null;
    let trailingArgs = null;

    return ((...args) => {
        const now = Date.now();
        const remaining = wait - (now - lastCallTime);
        trailingArgs = args;

        if (remaining <= 0) {
            if (timeoutId) {
                window.clearTimeout(timeoutId);
                timeoutId = null;
            }

            lastCallTime = now;
            callback(...trailingArgs);
            trailingArgs = null;
            return;
        }

        if (!timeoutId) {
            timeoutId = window.setTimeout(() => {
                lastCallTime = Date.now();
                timeoutId = null;
                callback(...(trailingArgs || []));
                trailingArgs = null;
            }, remaining);
        }
    });
};

/**
 * Return a debounced copy of a value.
 *
 * @template T
 * @param {T} value - Value to debounce.
 * @param {number} delay - Delay in milliseconds.
 * @returns {T} Debounced value.
 */
export const useDebouncedValue = (value, delay) => {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const timeoutId = window.setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => window.clearTimeout(timeoutId);
    }, [delay, value]);

    return debouncedValue;
};

/**
 * Manage shared job form state for create and edit screens.
 *
 * @param {object} initialValues - Initial form values.
 * @returns {object} Form state helpers.
 */
export const useJobFormState = (initialValues = JOB_FORM_DEFAULTS) => {
    const [values, setValues] = useState(initialValues);
    const [validationErrors, setValidationErrors] = useState({});
    const currentErrors = useMemo(() => validateJobForm(values), [values]);

    /**
     * Update a single field and remove its stale error message.
     *
     * @param {string} field - Field name.
     * @param {string} value - Updated field value.
     * @returns {void}
     */
    const handleFieldChange = (field, value) => {
        setValues((current) => ({ ...current, [field]: value }));
        setValidationErrors((current) => {
            if (!current[field]) return current;
            const nextErrors = { ...current };
            delete nextErrors[field];
            return nextErrors;
        });
    };

    return {
        currentErrors,
        handleFieldChange,
        setValidationErrors,
        setValues,
        validationErrors,
        values,
    };
};
