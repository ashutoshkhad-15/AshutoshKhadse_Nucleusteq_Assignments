import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import InterviewForm from '../components/interviews/InterviewForm';
import { interviewService } from '../services/interviewService';
import '../styles/interview-management.css';
import {
    buildInterviewPayload,
    getInterviewManagementErrorMessage,
    INTERVIEW_FORM_DEFAULTS,
    mapInterviewToFormValues,
    validateInterviewForm,
} from '../utils/interviewManagement';
import { loadInterviewDetails, loadInterviewFormOptions } from '../utils/pageLoaders';

/**
 * Render the interview edit workflow for HR users.
 */
const EditInterviewScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [values, setValues] = useState(INTERVIEW_FORM_DEFAULTS);
    const [validationErrors, setValidationErrors] = useState({});
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);
    const [candidateOptions, setCandidateOptions] = useState([]);
    const [jobOptions, setJobOptions] = useState([]);
    const [interviewerOptions, setInterviewerOptions] = useState([]);
    const [focusAreaDraft, setFocusAreaDraft] = useState('');
    const [interviewStatus, setInterviewStatus] = useState('');
    const isCompletedInterview = interviewStatus === 'INTERVIEW_COMPLETED';

    useEffect(() => {
        const controller = new AbortController();
        Promise.all([
            loadInterviewDetails(id, controller.signal),
            loadInterviewFormOptions(controller.signal),
            ])
            .then(([interviewResponse, formOptions]) => {
                const { candidateResponse, jobResponse, interviewerResponse } = formOptions;
                setValues(mapInterviewToFormValues(interviewResponse));
                setInterviewStatus(interviewResponse?.status || '');
                setCandidateOptions((Array.isArray(candidateResponse?.data) ? candidateResponse.data : []).map((candidate) => ({
                    value: candidate._id,
                    label: `${candidate.first_name || candidate.firstName || ''} ${candidate.last_name || candidate.lastName || ''}`.trim() || candidate.email,
                })));
                setJobOptions((Array.isArray(jobResponse?.data) ? jobResponse.data : []).map((job) => ({
                    value: job._id,
                    label: job.jobTitle || job.title || 'Untitled Job',
                })));
                setInterviewerOptions((Array.isArray(interviewerResponse?.data) ? interviewerResponse.data : [])
                    .filter((user) => user.role === 'INTERVIEWER')
                    .map((user) => ({
                    value: user._id,
                    label: user.name || user.email,
                })));
            })
            .catch((err) => {
                if (err?.name !== 'CanceledError') setError(getInterviewManagementErrorMessage(err, 'Failed to load interview details.'));
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

    const handleAddFocusArea = () => {
        const nextValue = focusAreaDraft.trim();
        if (!nextValue) {
            setValidationErrors((current) => ({ ...current, focusTechAreas: 'Focus Tech Areas are required.' }));
            return;
        }
        setValues((current) => {
            if (current.focusTechAreas.some((area) => area.toLowerCase() === nextValue.toLowerCase())) return current;
            return { ...current, focusTechAreas: [...current.focusTechAreas, nextValue] };
        });
        setFocusAreaDraft('');
    };

    const handleRemoveFocusArea = (area) => {
        setValues((current) => ({ ...current, focusTechAreas: current.focusTechAreas.filter((item) => item !== area) }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        const errors = validateInterviewForm(values);
        if (Object.keys(errors).length) {
            setValidationErrors(errors);
            return;
        }
        try {
            if (isCompletedInterview) {
                setError('Completed interviews cannot be edited.');
                return;
            }
            setSubmitting(true);
            const payload = buildInterviewPayload(values);
            await interviewService.updateInterview(id, payload);
            navigate('/interviews', { replace: true, state: { successMessage: 'Interview updated successfully.' } });
        } catch (err) {
            setError(getInterviewManagementErrorMessage(err, 'Failed to update interview.'));
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) return <div className="um-state">Loading interview details...</div>;

    return (
        <div className="um-container um-form-page">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Edit Interview</h1>
                    <p>Update the interview schedule details.</p>
                </div>
            </div>
            {isCompletedInterview ? <div className="error-banner">This interview is completed and cannot be edited.</div> : null}
            <InterviewForm
                values={values}
                validationErrors={validationErrors}
                formError={error}
                submitting={submitting}
                disabled={isCompletedInterview}
                submitLabel="Save Changes"
                submittingLabel="Saving..."
                candidateOptions={candidateOptions}
                jobOptions={jobOptions}
                interviewerOptions={interviewerOptions}
                onChange={handleChange}
                onCancel={() => navigate('/interviews')}
                onSubmit={handleSubmit}
                onAddFocusArea={handleAddFocusArea}
                onRemoveFocusArea={handleRemoveFocusArea}
                focusAreaDraft={focusAreaDraft}
                setFocusAreaDraft={setFocusAreaDraft}
            />
        </div>
    );
};

export default EditInterviewScreen;
