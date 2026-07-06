import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import CandidateForm from '../components/candidates/CandidateForm';
import { candidateService } from '../services/candidateService';
import '../styles/candidate-management.css';
import {
    buildCandidatePayload,
    getCandidateManagementErrorMessage,
    mapCandidateToFormValues,
    validateCandidateForm,
} from '../utils/candidateManagement';

const EditCandidateScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [values, setValues] = useState(mapCandidateToFormValues());
    const [selectedAppliedJob, setSelectedAppliedJob] = useState(null);
    const [validationErrors, setValidationErrors] = useState({});
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const controller = new AbortController();
        (async () => {
            try {
                const candidateResponse = await candidateService.getCandidateById(id, { signal: controller.signal });
                setValues(mapCandidateToFormValues(candidateResponse));
                setSelectedAppliedJob(candidateResponse?.applied_job ? {
                    value: candidateResponse.applied_job._id,
                    label: candidateResponse.applied_job.jobTitle,
                    description: 'Selected job',
                } : null);
            } catch (err) {
                if (err?.name !== 'CanceledError') setError(getCandidateManagementErrorMessage(err, 'Failed to load candidate details.'));
            } finally {
                if (!controller.signal.aborted) setLoading(false);
            }
        })();
        return () => controller.abort();
    }, [id]);

    const handleChange = (field, value, job) => {
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

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        const errors = validateCandidateForm(values);
        if (Object.keys(errors).length) {
            setValidationErrors(errors);
            return;
        }
        try {
            setSaving(true);
            const payload = buildCandidatePayload(values);
            await candidateService.updateCandidate(id, payload);
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
                    <p>Update candidate profile details and applied job selection.</p>
                </div>
            </div>
            <CandidateForm
                values={values}
                validationErrors={validationErrors}
                formError={error}
                submitting={saving}
                submitLabel="Save Changes"
                submittingLabel="Saving..."
                selectedAppliedJob={selectedAppliedJob}
                onChange={handleChange}
                onCancel={() => navigate('/candidates')}
                onSubmit={handleSubmit}
            />
        </div>
    );
};

export default EditCandidateScreen;
