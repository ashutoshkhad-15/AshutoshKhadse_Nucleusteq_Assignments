import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import InterviewForm from '../components/interviews/InterviewForm';
import '../styles/interview-management.css';
import {
    buildInterviewPayload,
    getInterviewManagementErrorMessage,
    INTERVIEW_FORM_DEFAULTS,
    validateInterviewForm,
} from '../utils/interviewManagement';
import { interviewService } from '../services/interviewService';
import { loadInterviewFormOptions } from '../utils/pageLoaders';

/**
 * Render the interview scheduling workflow.
 */
const ScheduleInterviewScreen = () => {
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

    useEffect(() => {
        const controller = new AbortController();
        loadInterviewFormOptions(controller.signal)
            .then(({ candidateResponse, jobResponse, interviewerResponse }) => {
                setCandidateOptions((Array.isArray(candidateResponse?.data) ? candidateResponse.data : [])
                    .filter((candidate) => (candidate.status || 'PROFILE_CREATED') !== 'REJECTED')
                    .map((candidate) => ({
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
                if (err?.name !== 'CanceledError') {
                    setError(getInterviewManagementErrorMessage(err, 'Failed to load interview form options.'));
                }
            })
            .finally(() => {
                if (!controller.signal.aborted) setLoading(false);
            });
        return () => controller.abort();
    }, []);

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
            if (current.focusTechAreas.some((area) => area.toLowerCase() === nextValue.toLowerCase())) {
                return current;
            }
            return { ...current, focusTechAreas: [...current.focusTechAreas, nextValue] };
        });
        setFocusAreaDraft('');
        setValidationErrors((current) => {
            if (!current.focusTechAreas) return current;
            const next = { ...current };
            delete next.focusTechAreas;
            return next;
        });
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
            setSubmitting(true);
            const payload = buildInterviewPayload(values);
            await interviewService.createInterview(payload);
            navigate('/interviews', { replace: true, state: { successMessage: 'Interview scheduled successfully.' } });
        } catch (err) {
            setError(getInterviewManagementErrorMessage(err, 'Failed to schedule interview.'));
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) return <div className="um-state">Loading interview form...</div>;

    return (
        <div className="um-container um-form-page">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Schedule Interview</h1>
                    <p>Create an interview slot for a candidate, job, and assigned interviewer.</p>
                </div>
            </div>
            <InterviewForm
                values={values}
                validationErrors={validationErrors}
                formError={error}
                submitting={submitting}
                submitLabel="Schedule Interview"
                submittingLabel="Scheduling..."
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

export default ScheduleInterviewScreen;
