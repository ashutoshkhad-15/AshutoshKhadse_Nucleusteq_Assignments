import { USER_ROLES } from '../constants/roles';
import { getStoredUserRole } from './session';

export const INTERVIEW_FORM_DEFAULTS = {
    candidateId: '',
    jobId: '',
    interviewDate: '',
    interviewTime: '',
    interviewerId: '',
    focusTechAreas: [],
};

export const FEEDBACK_FORM_DEFAULTS = {
    technicalRating: '',
    communicationRating: '',
    problemSolving: '',
    techAreasCovered: '',
    comments: '',
    recommendation: '',
};

export const RECOMMENDATION_OPTIONS = [
    { value: 'NEXT_ROUND', label: 'Next Round' },
    { value: 'SELECT', label: 'Select' },
    { value: 'REJECT', label: 'Reject' },
];

const normalizeText = (value) => (typeof value === 'string' ? value.trim().replace(/\s+/g, ' ') : '');

const normalizeList = (values) => {
    const source = Array.isArray(values) ? values : String(values).split(',');
    const deduped = [];
    source.forEach((value) => {
        const normalized = normalizeText(value);
        if (!normalized) return;
        if (deduped.some((item) => item.toLowerCase() === normalized.toLowerCase())) return;
        deduped.push(normalized);
    });
    return deduped;
};

/**
 * Build the interview payload for API submission.
 */
export const buildInterviewPayload = (values) => ({
    candidateId: values.candidateId,
    jobId: values.jobId,
    interviewDate: values.interviewDate,
    interviewTime: values.interviewTime,
    interviewerId: values.interviewerId,
    focusTechAreas: normalizeList(values.focusTechAreas),
});

/**
 * Map an interview record to form values.
 */
export const mapInterviewToFormValues = (interview = {}) => ({
    candidateId: interview.candidate_id || interview.candidateId || '',
    jobId: interview.job_id || interview.jobId || '',
    interviewDate: typeof interview.interview_date === 'string' ? interview.interview_date.slice(0, 10) : interview.interview_date || '',
    interviewTime: interview.interview_time || interview.interviewTime || '',
    interviewerId: interview.interviewer_id || interview.interviewerId || '',
    focusTechAreas: Array.isArray(interview.focus_tech_areas) ? interview.focus_tech_areas : interview.focusTechAreas || [],
});

/**
 * Build the feedback payload for API submission.
 */
export const buildFeedbackPayload = (values) => ({
    technicalRating: Number(values.technicalRating),
    communicationRating: Number(values.communicationRating),
    problemSolving: Number(values.problemSolving),
    techAreasCovered: normalizeList(values.techAreasCovered),
    comments: normalizeText(values.comments),
    recommendation: values.recommendation,
});

export const mapFeedbackToFormValues = (feedback = {}) => ({
    technicalRating: feedback.technical_rating ?? '',
    communicationRating: feedback.communication_rating ?? '',
    problemSolving: feedback.problem_solving ?? '',
    techAreasCovered: Array.isArray(feedback.tech_areas_covered) ? feedback.tech_areas_covered.join(', ') : '',
    comments: feedback.comments || '',
    recommendation: feedback.recommendation || '',
});

const isValidTime = (value) => /^(?:[01]?\d|2[0-3]):[0-5]\d$/.test(normalizeText(value));

const getCurrentIstDateTime = () => {
    const parts = new Intl.DateTimeFormat('en-CA', {
        timeZone: 'Asia/Kolkata',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
    }).formatToParts(new Date());

    const lookup = parts.reduce((acc, part) => {
        if (part.type !== 'literal') acc[part.type] = part.value;
        return acc;
    }, {});

    return {
        date: `${lookup.year}-${lookup.month}-${lookup.day}`,
        time: `${lookup.hour}:${lookup.minute}`,
    };
};

/**
 * Validate interview scheduling fields.
 */
export const validateInterviewForm = (values) => {
    const errors = {};
    const payload = buildInterviewPayload(values);
    const currentIst = getCurrentIstDateTime();

    if (!payload.candidateId) errors.candidateId = 'Candidate is required.';
    if (!payload.jobId) errors.jobId = 'Job Title is required.';
    if (!payload.interviewerId) errors.interviewerId = 'Assigned Interviewer is required.';
    if (!payload.interviewDate) errors.interviewDate = 'Interview Date is required.';
    if (payload.interviewDate && payload.interviewDate < currentIst.date) {
        errors.interviewDate = 'Interview date cannot be in the past.';
    }
    if (!payload.interviewTime) errors.interviewTime = 'Interview Time is required.';
    else if (!isValidTime(payload.interviewTime)) errors.interviewTime = 'Interview Time must use HH:MM in 24-hour format.';
    else if (payload.interviewDate === currentIst.date && payload.interviewTime <= currentIst.time) {
        errors.interviewTime = 'Interview time must be in the future.';
    }
    if (!payload.focusTechAreas.length) errors.focusTechAreas = 'Focus Tech Areas are required.';

    return errors;
};

/**
 * Validate interview feedback fields.
 */
export const validateFeedbackForm = (values) => {
    const errors = {};
    const payload = buildFeedbackPayload(values);

    ['technicalRating', 'communicationRating', 'problemSolving'].forEach((field) => {
        if (payload[field] === '' || Number.isNaN(payload[field])) {
            errors[field] = 'Rating is required.';
        } else if (payload[field] < 1 || payload[field] > 5) {
            errors[field] = 'Rating must be between 1 and 5.';
        }
    });

    if (!payload.recommendation) errors.recommendation = 'Recommendation is required.';
    if (!payload.techAreasCovered.length) errors.techAreasCovered = 'Tech Areas Covered are required.';
    if (!normalizeText(payload.comments)) errors.comments = 'Comments are required.';

    return errors;
};

/**
 * Normalize API failures into a single message for interview screens.
 */
export const getInterviewManagementErrorMessage = (error, fallbackMessage) =>
    error?.response?.data?.details?.[0]?.msg || error?.response?.data?.message || fallbackMessage;

/**
 * Format a date value for display.
 */
export const formatInterviewDate = (value) => {
    if (!value) return 'Not available';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return 'Not available';
    return new Intl.DateTimeFormat('en-GB', {
        timeZone: 'Asia/Kolkata',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
    }).format(date);
};

/**
 * Format a time value for display.
 */
export const formatInterviewTime = (value) => normalizeText(value) || 'Not available';

/**
 * Return the current portal role from local storage.
 */
export const getCurrentRole = () => getStoredUserRole();

/**
 * Check whether the current user can manage interviews.
 */
export const canManageInterviews = () => [USER_ROLES.HR, USER_ROLES.ADMIN].includes(getCurrentRole());

/**
 * Check whether the current user can view interview records.
 */
export const canViewInterviews = () => [USER_ROLES.HR, USER_ROLES.ADMIN, USER_ROLES.INTERVIEWER].includes(getCurrentRole());

/**
 * Check whether the current user can view dashboard information.
 */
export const canViewDashboard = () => [USER_ROLES.HR, USER_ROLES.ADMIN, USER_ROLES.INTERVIEWER].includes(getCurrentRole());

/**
 * Throttle a callback to run at most once per wait interval.
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
