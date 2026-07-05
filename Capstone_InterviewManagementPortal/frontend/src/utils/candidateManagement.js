export const CANDIDATE_FORM_DEFAULTS = {
    firstName: '',
    lastName: '',
    email: '',
    mobile: '',
    currentCompany: '',
    totalExperience: '',
    appliedJobId: '',
};

export const CANDIDATE_SEARCH_DEBOUNCE_MS = 500;

export const TOTAL_EXPERIENCE_PATTERN =
  /^(?:\d+ year|\d+ years|\d+\+ years|\d+-\d+ years)$/;

const NAME_PATTERN = /^(?=.*[A-Za-z])[A-Za-z]+(?: [A-Za-z]+)*$/;
const EMAIL_PATTERN = /^(?!\.)(?!.*\.\.)[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*@(gmail\.com|outlook\.com|yahoo\.com)$/i;
const MOBILE_PATTERN = /^\d{10}$/;
const COMPANY_PATTERN = /^(?=.*[A-Za-z])[A-Za-z0-9][A-Za-z0-9\s&().,'/-]*[A-Za-z0-9]$/;

export const mapCandidateToFormValues = (candidate = {}) => ({
    firstName: candidate.first_name || candidate.firstName || '',
    lastName: candidate.last_name || candidate.lastName || '',
    email: candidate.email || '',
    mobile: candidate.mobile || '',
    currentCompany: candidate.current_company || candidate.currentCompany || '',
    totalExperience: candidate.total_experience || candidate.totalExperience || '',
    appliedJobId: candidate.applied_job_id || candidate.appliedJobId || candidate.applied_job?._id || '',
});

export const buildCandidatePayload = (values) => ({
    firstName: values.firstName.trim(),
    lastName: values.lastName.trim(),
    email: values.email.trim().toLowerCase(),
    mobile: values.mobile.trim(),
    currentCompany: values.currentCompany.trim(),
    totalExperience: values.totalExperience.trim(),
    appliedJobId: values.appliedJobId,
});

const validateName = (value, label) => {
    const normalized = typeof value === 'string' ? value.trim() : '';
    if (!normalized) {
        return `${label} is required.`;
    }
    if (normalized.length < 2 || normalized.length > 50) {
        return `${label} must be between 2 and 50 characters.`;
    }
    if (!NAME_PATTERN.test(normalized)) {
        return `${label} can contain alphabetic characters and single spaces only.`;
    }
    return '';
};

export const validateCandidateForm = (values) => {
    const errors = {};
    const payload = buildCandidatePayload(values);

    const firstNameError = validateName(payload.firstName, 'First Name');
    if (firstNameError) errors.firstName = firstNameError;

    const lastNameError = validateName(payload.lastName, 'Last Name');
    if (lastNameError) errors.lastName = lastNameError;

    if (!payload.email) {
        errors.email = 'Email is required.';
    } else if (!EMAIL_PATTERN.test(payload.email)) {
        errors.email = 'Email Address must be a valid gmail.com, outlook.com, or yahoo.com address using only letters, numbers, and single dots.';
    }

    if (!payload.mobile) {
        errors.mobile = 'Mobile number is required.';
    } else if (!MOBILE_PATTERN.test(payload.mobile)) {
        errors.mobile = 'Mobile number must contain exactly 10 digits.';
    }

    if (!payload.currentCompany) {
        errors.currentCompany = 'Current Company is required.';
    } else if (payload.currentCompany.length > 120) {
        errors.currentCompany = 'Current Company must be at most 120 characters.';
    } else if (payload.currentCompany && !COMPANY_PATTERN.test(payload.currentCompany)) {
        errors.currentCompany = 'Current Company must contain alphabetic characters and may include spaces and common punctuation.';
    }

    if (!payload.totalExperience) {
        errors.totalExperience = 'Total Experience is required.';
    } else if (!TOTAL_EXPERIENCE_PATTERN.test(payload.totalExperience)) {
        errors.totalExperience = 'Use formats like "0 year", "1 year", "2 years", "3+ years", or "5-7 years".';
    }

    if (!payload.appliedJobId) {
        errors.appliedJobId = 'Applied Job is required.';
    }

    return errors;
};

export const getCandidateManagementErrorMessage = (error, fallbackMessage) =>
    error?.response?.data?.details?.[0]?.msg || error?.response?.data?.message || fallbackMessage;

export const getCandidateAppliedJobLabel = (candidate) => candidate?.applied_job?.jobTitle || candidate?.appliedJob?.jobTitle || candidate?.applied_job?.job_title || 'Not specified';

export const formatCandidateDate = (value) => {
    if (!value) return 'Not available';
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? 'Not available' : date.toLocaleDateString();
};

export const mapJobsToOptions = (jobs = []) =>
    jobs.map((job) => ({
        value: job._id,
        label: job.jobTitle || job.title || 'Untitled Job',
        description: job.jobRole || job.location || '',
    }));
