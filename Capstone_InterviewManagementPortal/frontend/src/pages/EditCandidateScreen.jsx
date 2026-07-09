import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import CandidateForm from '../components/candidates/CandidateForm';
import { candidateService } from '../services/candidateService';
import '../styles/candidate-management.css';
import {
    buildCandidatePayload,
    CANDIDATE_STATUS_OPTIONS,
    getCandidateManagementErrorMessage,
    mapCandidateToFormValues,
    mapAppliedJobToOption,
    MAX_RESUME_FILE_SIZE_BYTES,
    validateCandidateForm,
} from '../utils/candidateManagement';
import { loadCandidateDetails } from '../utils/pageLoaders';

/**
 * Render the candidate edit screen with resume and status controls.
 */
const EditCandidateScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [values, setValues] = useState(mapCandidateToFormValues());
    const [selectedAppliedJob, setSelectedAppliedJob] = useState(null);
    const [validationErrors, setValidationErrors] = useState({});
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);
    const [resumeFile, setResumeFile] = useState(null);
    const [resumeError, setResumeError] = useState('');
    const [statusValue, setStatusValue] = useState('PROFILE_CREATED');
    const [initialStatus, setInitialStatus] = useState('PROFILE_CREATED');

    useEffect(() => {
        const controller = new AbortController();
        loadCandidateDetails(id, controller.signal)
            .then((candidateResponse) => {
                setValues(mapCandidateToFormValues(candidateResponse));
                const currentStatus = candidateResponse?.status || 'PROFILE_CREATED';
                setStatusValue(currentStatus);
                setInitialStatus(currentStatus);
                setSelectedAppliedJob(mapAppliedJobToOption(candidateResponse?.applied_job));
            })
            .catch((err) => {
                if (err?.name !== 'CanceledError') setError(getCandidateManagementErrorMessage(err, 'Failed to load candidate details.'));
            })
            .finally(() => {
                if (!controller.signal.aborted) setLoading(false);
            });
        return () => controller.abort();
    }, [id]);

    const handleChange = (field, value, job) => {
        if (field === 'status') {
            setStatusValue(value);
            return;
        }
        setValues((current) => ({ ...current, [field]: value }));
        if (field === 'appliedJobId') {
            setSelectedAppliedJob(job || null);
        }
        setValidationErrors((current) => {
            if (!current[field]) return current;
            const next = { ...current };
            delete next[field];
            return next;
        });
    };

    const validateResumeFile = (file) => {
        if (!file) return '';
        if (!file.name?.toLowerCase().endsWith('.pdf')) return 'Only PDF files are allowed.';
        if ((file.type || '').toLowerCase() !== 'application/pdf') return 'Only PDF files are allowed.';
        if (file.size === 0) return 'Resume is required.';
        if (file.size > MAX_RESUME_FILE_SIZE_BYTES) return 'Resume size cannot exceed 5 MB.';
        return '';
    };

    const handleResumeFileChange = (event) => {
        const file = event.target.files?.[0] || null;
        setResumeFile(file);
        setResumeError('');
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        const errors = validateCandidateForm(values);
        if (Object.keys(errors).length) {
            setValidationErrors(errors);
            return;
        }
        const resumeValidationError = validateResumeFile(resumeFile);
        if (resumeValidationError) {
            setResumeError(resumeValidationError);
            return;
        }
        try {
            setSaving(true);
            const payload = buildCandidatePayload(values);
            await candidateService.updateCandidate(id, payload);
            if (statusValue !== initialStatus) {
                await candidateService.updateCandidateStatus(id, statusValue);
            }
            if (resumeFile) {
                const formData = new FormData();
                formData.append('resume_file', resumeFile);
                try {
                    await candidateService.uploadResume(id, formData);
                    setResumeFile(null);
                } catch (uploadError) {
                    setResumeError(getCandidateManagementErrorMessage(uploadError, 'Failed to upload resume.'));
                    return;
                }
            }
            navigate('/candidates', { replace: true, state: { successMessage: 'Candidate updated successfully.' } });
        } catch (err) {
            setError(getCandidateManagementErrorMessage(err, 'Failed to update candidate.'));
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <div className="um-state">Loading candidate details...</div>;

    return (
        <div className="um-container um-form-page">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Edit Candidate</h1>
                    <p>Update candidate profile details, resume, and status.</p>
                </div>
            </div>
            <CandidateForm
                values={values}
                validationErrors={validationErrors}
                formError={error}
                submitting={saving}
                submitLabel="Save Changes"
                submittingLabel="Saving..."
                statusLabel={statusValue}
                statusOptions={CANDIDATE_STATUS_OPTIONS}
                resumeFile={resumeFile}
                resumeError={resumeError}
                onResumeFileChange={handleResumeFileChange}
                onChange={handleChange}
                onCancel={() => navigate('/candidates')}
                onSubmit={handleSubmit}
                selectedAppliedJob={selectedAppliedJob}
            />
        </div>
    );
};

export default EditCandidateScreen;
