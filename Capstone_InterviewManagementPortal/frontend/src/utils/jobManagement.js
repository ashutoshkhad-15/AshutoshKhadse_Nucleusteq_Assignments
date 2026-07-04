import { useMemo, useState } from 'react';

export const JOB_FORM_DEFAULTS = {
    jobTitle: '',
    jobDetails: '',
    jobRole: '',
    requiredSkills: [],
    experienceRequired: '',
    employmentType: '',
    location: '',
};

export const EMPLOYMENT_TYPE_OPTIONS = [
    { value: 'Full Time', label: 'Full Time' },
    { value: 'Internship', label: 'Internship' },
];

export const JOB_LIST_SKELETON_COUNT = 6;
export const JOB_SEARCH_DEBOUNCE_MS = 500;
export const JOB_TEXT_MIN_LENGTH = {
    jobTitle: 3,
    jobDetails: 10,
    jobRole: 2,
    location: 2,
};
export const JOB_TEXT_MAX_LENGTH = {
    jobTitle: 120,
    jobDetails: 4000,
    jobRole: 80,
    location: 120,
};
export const EXPERIENCE_REQUIRED_PATTERN = /^(?:\d{1,2}\s+year|\d{1,2}\s+years|\d{1,2}\+\s+years|\d{1,2}-\d{1,2}\s+years)$/;

const normalizeText = (value) => (typeof value === 'string' ? value.trim() : '');

export const normalizeSkills = (skills = []) => {
    const source = Array.isArray(skills) ? skills : String(skills).split(/[\n,]/);
    const deduped = [];
    source.forEach((skill) => {
        const normalized = normalizeText(skill).replace(/\s+/g, ' ');
        if (!normalized || deduped.some((item) => item.toLowerCase() === normalized.toLowerCase())) {
            return;
        }
        deduped.push(normalized);
    });
    return deduped;
};

export const normalizeExperienceRequired = (value) => normalizeText(value);

export const mapJobToFormValues = (job = {}) => ({
    jobTitle: job.jobTitle || job.title || '',
    jobDetails: job.jobDetails || job.description || '',
    jobRole: job.jobRole || job.department || '',
    requiredSkills: normalizeSkills(job.requiredSkills || job.skills || []),
    experienceRequired: normalizeExperienceRequired(job.experienceRequired ?? job.experience_required ?? ''),
    employmentType: job.employmentType || job.employment_type || '',
    location: job.location || '',
});

export const buildJobPayload = (values) => ({
    jobTitle: normalizeText(values.jobTitle),
    jobDetails: normalizeText(values.jobDetails),
    jobRole: normalizeText(values.jobRole),
    requiredSkills: normalizeSkills(values.requiredSkills),
    experienceRequired: normalizeExperienceRequired(values.experienceRequired),
    employmentType: values.employmentType,
    location: normalizeText(values.location),
});

const validateTextField = (value, fieldName, minLength, maxLength) => {
    const normalized = normalizeText(value);
    if (!normalized) {
        return `${fieldName} is required.`;
    }
    if (normalized.length < minLength || normalized.length > maxLength) {
        return `${fieldName} must be between ${minLength} and ${maxLength} characters.`;
    }
    return '';
};

export const validateJobForm = (values) => {
    const errors = {};
    const payload = buildJobPayload(values);

    const jobTitleError = validateTextField(payload.jobTitle, 'Job Title', JOB_TEXT_MIN_LENGTH.jobTitle, JOB_TEXT_MAX_LENGTH.jobTitle);
    if (jobTitleError) errors.jobTitle = jobTitleError;

    const jobDetailsError = validateTextField(payload.jobDetails, 'Job Details', JOB_TEXT_MIN_LENGTH.jobDetails, JOB_TEXT_MAX_LENGTH.jobDetails);
    if (jobDetailsError) errors.jobDetails = jobDetailsError;

    const jobRoleError = validateTextField(payload.jobRole, 'Job Role', JOB_TEXT_MIN_LENGTH.jobRole, JOB_TEXT_MAX_LENGTH.jobRole);
    if (jobRoleError) errors.jobRole = jobRoleError;

    if (!payload.requiredSkills.length) {
        errors.requiredSkills = 'At least one required skill is needed.';
    }

    if (!payload.experienceRequired) {
        errors.experienceRequired = 'Experience Required is required.';
    } else if (!EXPERIENCE_REQUIRED_PATTERN.test(payload.experienceRequired)) {
        errors.experienceRequired = 'Use formats like "0 year", "1 year", "2 years", "3+ years", or "5-7 years".';
    }

    if (!payload.employmentType) {
        errors.employmentType = 'Employment Type is required.';
    }

    const locationError = validateTextField(payload.location, 'Location', JOB_TEXT_MIN_LENGTH.location, JOB_TEXT_MAX_LENGTH.location);
    if (locationError) errors.location = locationError;

    return errors;
};

export const getJobManagementErrorMessage = (error, fallbackMessage) => error?.response?.data?.details?.[0]?.msg || error?.response?.data?.message || fallbackMessage;

export const throttle = (callback, wait) => {
    let lastCallTime = 0;
    let timeoutId = null;
    let trailingArgs = null;
    return ((...args) => {
        const now = Date.now();
        const remaining = wait - (now - lastCallTime);
        trailingArgs = args;
        if (remaining <= 0) {
            if (timeoutId) window.clearTimeout(timeoutId);
            timeoutId = null;
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

export const useJobFormState = (initialValues = JOB_FORM_DEFAULTS) => {
    const [values, setValues] = useState(initialValues);
    const [validationErrors, setValidationErrors] = useState({});
    const currentErrors = useMemo(() => validateJobForm(values), [values]);

    const handleFieldChange = (field, value) => {
        setValues((current) => ({ ...current, [field]: value }));
        setValidationErrors((current) => {
            if (!current[field]) return current;
            const next = { ...current };
            delete next[field];
            return next;
        });
    };

    const addSkill = (skill) => {
        const normalized = normalizeText(skill).replace(/\s+/g, ' ');
        if (!normalized) return;
        setValues((current) => ({ ...current, requiredSkills: normalizeSkills([...current.requiredSkills, normalized]) }));
    };

    const removeSkill = (skill) => {
        setValues((current) => ({ ...current, requiredSkills: current.requiredSkills.filter((item) => item !== skill) }));
    };

    return { currentErrors, handleFieldChange, removeSkill, addSkill, setValidationErrors, setValues, validationErrors, values };
};
