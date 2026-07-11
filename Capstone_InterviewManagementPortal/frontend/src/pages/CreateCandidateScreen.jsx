import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CandidateForm from '../components/candidates/CandidateForm';
import { candidateService } from '../services/candidateService';
import '../styles/candidate-management.css';
import {
    buildCandidatePayload,
    CANDIDATE_FORM_DEFAULTS,
    MAX_RESUME_FILE_SIZE_BYTES,
    getCandidateManagementErrorMessage,
    validateCandidateForm,
} from '../utils/candidateManagement';

const CreateCandidateScreen = () => {
    const navigate = useNavigate();
    const [values, setValues] = useState(CANDIDATE_FORM_DEFAULTS);
    const [validationErrors, setValidationErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [resumeFile, setResumeFile] = useState(null);
    const [resumeError, setResumeError] = useState('');

    const handleChange = (field, value) => {
        setValues((current) => ({ ...current, [field]: value }));
        setValidationErrors((current) => {
            if (!current[field]) return current;
            const next = { ...current };
            delete next[field];
            return next;
        });
    };

    /**
     * Validate the selected resume file.
     */
    const validateResumeFile = (file) => {
        if (!file) return '';
        if (!file.name?.toLowerCase().endsWith('.pdf')) return 'Only PDF files are allowed.';
        if ((file.type || '').toLowerCase() !== 'application/pdf') return 'Only PDF files are allowed.';
        if (file.size === 0) return 'Resume is required.';
        if (file.size > MAX_RESUME_FILE_SIZE_BYTES) return 'Resume size cannot exceed 5 MB.';
        return '';
    };

    /**
     * Handle resume selection on create.
     */
    const handleResumeFileChange = (event) => {
        const file = event.target.files?.[0] || null;
        setResumeFile(file);
        setResumeError('');
    };

    /**
     * Create the candidate and upload the selected resume if present.
     */
    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        setResumeError('');
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
            setLoading(true);
            const payload = buildCandidatePayload(values);
            const createdCandidate = await candidateService.createCandidate(payload);
            if (resumeFile && createdCandidate?._id) {
                try {
                    const formData = new FormData();
                    formData.append('resume_file', resumeFile);
                    await candidateService.uploadResume(createdCandidate._id, formData);
                } catch (uploadError) {
                    setResumeError(getCandidateManagementErrorMessage(uploadError, 'Failed to upload resume.'));
                    return;
                }
            }
            navigate('/candidates', { replace: true, state: { successMessage: 'Candidate registered successfully.' } });
        } catch (err) {
            setError(getCandidateManagementErrorMessage(err, 'Failed to register candidate. Please try again.'));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="um-container um-form-page">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Register Candidate</h1>
                    <p>Create a new candidate profile for interview tracking and workflow management.</p>
                </div>
            </div>
            <CandidateForm
                values={values}
                validationErrors={validationErrors}
                formError={error}
                submitting={loading}
                submitLabel="Register Candidate"
                submittingLabel="Registering..."
                statusLabel="PROFILE_CREATED"
                statusReadOnly
                resumeFile={resumeFile}
                resumeError={resumeError}
                onResumeFileChange={handleResumeFileChange}
                onChange={handleChange}
                onCancel={() => navigate('/candidates')}
                onSubmit={handleSubmit}
            />
        </div>
    );
};

export default CreateCandidateScreen;
