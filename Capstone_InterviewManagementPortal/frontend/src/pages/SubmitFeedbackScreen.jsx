import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import FeedbackForm from '../components/interviews/FeedbackForm';
import { interviewService } from '../services/interviewService';
import '../styles/interview-management.css';
import {
    buildFeedbackPayload,
    FEEDBACK_FORM_DEFAULTS,
    getInterviewManagementErrorMessage,
    mapFeedbackToFormValues,
    validateFeedbackForm,
} from '../utils/interviewManagement';
import { USER_ROLES } from '../constants/roles';
import { ROUTES } from '../constants/routes';
import { loadInterviewFeedbackForm } from '../utils/pageLoaders';
import { getStoredUserRole } from '../utils/session';

/**
 * Render the feedback submission workflow.
 */
const SubmitFeedbackScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const role = getStoredUserRole();
    const [values, setValues] = useState(FEEDBACK_FORM_DEFAULTS);
    const [validationErrors, setValidationErrors] = useState({});
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);
    const [interview, setInterview] = useState(null);
    const [feedback, setFeedback] = useState(null);
    const canSubmitFeedback = interview?.status === 'INTERVIEW_COMPLETED';

    useEffect(() => {
        const controller = new AbortController();
        loadInterviewFeedbackForm(id, controller.signal)
            .then(({ interviewData, feedbackData }) => {
                setInterview(interviewData);
                setFeedback(feedbackData);
                if (feedbackData?.feedback) {
                    setValues(mapFeedbackToFormValues(feedbackData.feedback));
                }
            })
            .catch((err) => {
                if (err?.name !== 'CanceledError') setError(getInterviewManagementErrorMessage(err, 'Failed to load interview feedback form.'));
            })
            .finally(() => {
                if (!controller.signal.aborted) setLoading(false);
            });
        return () => controller.abort();
    }, [id]);

    const handleChange = (field, value) => {
        setValues((current) => ({ ...current, [field]: value }));
        setValidationErrors((current) => {
            if (!current[field]) return current;
            const next = { ...current };
            delete next[field];
            return next;
        });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        const errors = validateFeedbackForm(values);
        if (Object.keys(errors).length) {
            setValidationErrors(errors);
            return;
        }
        if (!canSubmitFeedback) {
            setError('Feedback can only be submitted after the interview is completed.');
            return;
        }
        try {
            setSubmitting(true);
            const payload = buildFeedbackPayload(values);
            await interviewService.submitFeedback(id, payload);
            navigate(ROUTES.INTERVIEW_ASSIGNED, { replace: true, state: { successMessage: 'Feedback submitted successfully.' } });
        } catch (err) {
            setError(getInterviewManagementErrorMessage(err, 'Failed to submit feedback.'));
        } finally {
            setSubmitting(false);
        }
    };

    const renderSubmittedFeedback = () => (
        <div className="form-card">
            <div className="form-section-title">Feedback Submitted</div>
            <div className="jm-detail-grid">
                <div className="jm-detail-item"><span className="jm-detail-label">Technical Rating</span><span className="jm-detail-value">{feedback.feedback.technical_rating}</span></div>
                <div className="jm-detail-item"><span className="jm-detail-label">Communication Rating</span><span className="jm-detail-value">{feedback.feedback.communication_rating}</span></div>
                <div className="jm-detail-item"><span className="jm-detail-label">Problem Solving</span><span className="jm-detail-value">{feedback.feedback.problem_solving}</span></div>
                <div className="jm-detail-item"><span className="jm-detail-label">Tech Areas Covered</span><span className="jm-detail-value">{(feedback.feedback.tech_areas_covered || []).join(', ') || 'Not available'}</span></div>
                <div className="jm-detail-item"><span className="jm-detail-label">Comments</span><span className="jm-detail-value">{feedback.feedback.comments || 'Not available'}</span></div>
                <div className="jm-detail-item"><span className="jm-detail-label">Recommendation</span><span className="jm-detail-value">{feedback.feedback.recommendation}</span></div>
            </div>
            <div className="form-actions">
                <button type="button" onClick={() => navigate(ROUTES.INTERVIEW_ASSIGNED)} className="btn-secondary">Back</button>
            </div>
        </div>
    );

    if (loading) return <div className="um-state">Loading feedback form...</div>;

    if (role !== USER_ROLES.INTERVIEWER) {
        return (
            <div className="um-container">
                <div className="um-header">
                    <div className="um-title-group">
                        <p className="um-eyebrow">Hiring</p>
                        <h1>Feedback</h1>
                        <p>{interview ? `${interview.candidate_name} | ${interview.job_title}` : 'Interview feedback'}</p>
                    </div>
                    <button type="button" onClick={() => navigate(`/interviews/${id}`)} className="btn-secondary">Back</button>
                </div>
                <div className="table-card">
                    {feedback?.feedback ? (
                        <table className="um-table">
                            <thead>
                                <tr>
                                    <th>Field</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td data-label="Field">Technical Rating</td><td data-label="Value">{feedback.feedback.technical_rating}</td></tr>
                                <tr><td data-label="Field">Communication Rating</td><td data-label="Value">{feedback.feedback.communication_rating}</td></tr>
                                <tr><td data-label="Field">Problem Solving</td><td data-label="Value">{feedback.feedback.problem_solving}</td></tr>
                                <tr><td data-label="Field">Tech Areas Covered</td><td data-label="Value">{(feedback.feedback.tech_areas_covered || []).join(', ')}</td></tr>
                                <tr><td data-label="Field">Comments</td><td data-label="Value">{feedback.feedback.comments || 'Not available'}</td></tr>
                                <tr><td data-label="Field">Recommendation</td><td data-label="Value">{feedback.feedback.recommendation}</td></tr>
                            </tbody>
                        </table>
                    ) : (
                        <div className="empty-state">No feedback has been submitted for this interview.</div>
                    )}
                </div>
            </div>
        );
    }

    return (
        <div className="um-container um-form-page">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Submit Feedback</h1>
                    <p>{interview ? `${interview.candidate_name} | ${interview.job_title}` : 'Interview feedback'}</p>
                </div>
            </div>
            {!canSubmitFeedback ? <div className="error-banner">Feedback can only be submitted after the interview is completed.</div> : null}
            {canSubmitFeedback && !feedback?.feedback ? <div className="empty-state">No feedback has been submitted yet for this interview.</div> : null}
            {feedback?.feedback ? renderSubmittedFeedback() : (
                <FeedbackForm
                    values={values}
                    validationErrors={validationErrors}
                    formError={error}
                    submitting={submitting}
                    submitLabel="Submit Feedback"
                    submittingLabel="Submitting..."
                    onChange={handleChange}
                    onCancel={() => navigate(ROUTES.INTERVIEW_ASSIGNED)}
                    onSubmit={handleSubmit}
                    disabled={!canSubmitFeedback}
                />
            )}
        </div>
    );
};

export default SubmitFeedbackScreen;
