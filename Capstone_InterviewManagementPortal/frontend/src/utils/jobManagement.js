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

export const JOB_LIST_SKELETON_COUNT = 6;
export const JOB_SEARCH_DEBOUNCE_MS = 500;

export const EMPLOYMENT_TYPE_OPTIONS = [
    { value: 'Full Time', label: 'Full Time' },
    { value: 'Internship', label: 'Internship' },
];

export const JOB_TEXT_MIN_LENGTH = {
    jobTitle: 3,
    jobDetails: 20,
    jobRole: 2,
    location: 2,
    skill: 2,
};

export const JOB_TEXT_MAX_LENGTH = {
    jobTitle: 100,
    jobDetails: 1000,
    jobRole: 60,
    location: 80,
    skill: 30,
};

export const EXPERIENCE_REQUIRED_PATTERN = /^(?:\d+ month|\d+ months|\d+ year|\d+ years|\d+ year \d+ month|\d+ year \d+ months|\d+ years \d+ month|\d+ years \d+ months|\d+\+ years|\d+-\d+ years)$/;
export const JOB_TITLE_PATTERN = /^(?=.*[A-Za-z])[A-Za-z0-9&()/+\- ]{3,100}$/;
export const JOB_ROLE_PATTERN = /^(?=.*[A-Za-z])[A-Za-z0-9 ]{2,60}$/;
export const LOCATION_PATTERN = /^(?=.*[A-Za-z])[A-Za-z0-9.,'()\- ]{2,80}$/;

const normalizeText = (value) => (typeof value === 'string' ? value.trim().replace(/\s+/g, ' ') : '');

const hasAlphabetic = (value) => /[A-Za-z]/.test(value);

export const validateSkillText = (value) => {
    const normalized = normalizeText(value);
    if (!normalized) return 'Skill is required.';
    if (normalized.length < 2 || normalized.length > 30) return 'Skill must be between 2 and 30 characters.';
    if (!hasAlphabetic(normalized)) return 'Skill must contain at least one alphabetic character.';
    if (!/^[A-Za-z0-9 .&()/+-]+$/.test(normalized)) return 'Skill can contain letters, numbers, spaces, and common symbols only.';
    return '';
};

export const normalizeSkills = (skills = []) => {
    const source = Array.isArray(skills) ? skills : String(skills).split(/[\n,]/);
    const deduped = [];
    source.forEach((skill) => {
        const normalized = normalizeText(skill);
        if (!normalized || deduped.some((item) => item.toLowerCase() === normalized.toLowerCase())) return;
        if (validateSkillText(normalized)) return;
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

const validateTextField = (value, fieldName, minLength, maxLength, pattern, invalidMessage) => {
    const normalized = normalizeText(value);
    if (!normalized) return `${fieldName} is required.`;
    if (normalized.length < minLength || normalized.length > maxLength) {
        return `${fieldName} must be between ${minLength} and ${maxLength} characters.`;
    }
    if (pattern && !pattern.test(normalized)) return invalidMessage;
    return '';
};

export const validateJobForm = (values) => {
    const errors = {};
    const payload = buildJobPayload(values);

    const jobTitleError = validateTextField(
        payload.jobTitle,
        'Job Title',
        JOB_TEXT_MIN_LENGTH.jobTitle,
        JOB_TEXT_MAX_LENGTH.jobTitle,
        JOB_TITLE_PATTERN,
        'Job Title must contain at least one letter and may include numbers, spaces, and symbols like - / & ( ) +.',
    );
    if (jobTitleError) errors.jobTitle = jobTitleError;

    const jobRoleError = validateTextField(
        payload.jobRole,
        'Job Role',
        JOB_TEXT_MIN_LENGTH.jobRole,
        JOB_TEXT_MAX_LENGTH.jobRole,
        JOB_ROLE_PATTERN,
        'Job Role must contain letters and can include digits and spaces only.',
    );
    if (jobRoleError) errors.jobRole = jobRoleError;

    const jobDetailsError = validateTextField(payload.jobDetails, 'Job Details', JOB_TEXT_MIN_LENGTH.jobDetails, JOB_TEXT_MAX_LENGTH.jobDetails);
    if (jobDetailsError) errors.jobDetails = jobDetailsError;

    if (!payload.requiredSkills.length) {
        errors.requiredSkills = 'At least one required skill is needed.';
    } else if (payload.requiredSkills.length > 20) {
        errors.requiredSkills = 'A maximum of 20 skills is allowed.';
    } else if (payload.requiredSkills.some((skill) => validateSkillText(skill))) {
        errors.requiredSkills = 'Each skill must be 2 to 30 characters and include at least one letter.';
    }

    if (!payload.experienceRequired) {
        errors.experienceRequired = 'Experience Required is required.';
    } else if (!EXPERIENCE_REQUIRED_PATTERN.test(payload.experienceRequired)) {
        errors.experienceRequired = "Experience must be in one of these formats: '3 months', '1 year', '3 years', '3 year 6 months', '3+ years', or '3-5 years'.";
    }

    if (!payload.employmentType) {
        errors.employmentType = 'Employment Type is required.';
    }

    const locationError = validateTextField(
        payload.location,
        'Location',
        JOB_TEXT_MIN_LENGTH.location,
        JOB_TEXT_MAX_LENGTH.location,
        LOCATION_PATTERN,
        'Location must contain at least one alphabetic character and may include commas, periods, hyphens, apostrophes, parentheses, and spaces.',
    );
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
        const normalized = normalizeText(skill);
        if (!normalized) return 'Skill is required.';
        const validationError = validateSkillText(normalized);
        if (validationError) return validationError;
        setValues((current) => ({ ...current, requiredSkills: normalizeSkills([...current.requiredSkills, normalized]) }));
        return '';
    };

    const removeSkill = (skill) => {
        setValues((current) => ({ ...current, requiredSkills: current.requiredSkills.filter((item) => item !== skill) }));
    };

    return { currentErrors, handleFieldChange, removeSkill, addSkill, setValidationErrors, setValues, validationErrors, values };
};
