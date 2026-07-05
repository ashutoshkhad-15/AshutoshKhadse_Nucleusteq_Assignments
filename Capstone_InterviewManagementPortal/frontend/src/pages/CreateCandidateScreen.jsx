import { Plus } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CandidateForm from '../components/candidates/CandidateForm';
import { candidateService } from '../services/candidateService';
import '../styles/candidate-management.css';
import {
    buildCandidatePayload,
    CANDIDATE_FORM_DEFAULTS,
    getCandidateManagementErrorMessage,
    validateCandidateForm,
} from '../utils/candidateManagement';

const CreateCandidateScreen = () => {
    const navigate = useNavigate();
    const [values, setValues] = useState(CANDIDATE_FORM_DEFAULTS);
    const [validationErrors, setValidationErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

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
        const errors = validateCandidateForm(values);
        if (Object.keys(errors).length) {
            setValidationErrors(errors);
            return;
        }
        try {
            setLoading(true);
            const payload = buildCandidatePayload(values);
            await candidateService.createCandidate(payload);
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
                <span className="jm-header-pill"><Plus size={16} aria-hidden="true" /> Candidate Intake</span>
            </div>
            <CandidateForm
                values={values}
                validationErrors={validationErrors}
                formError={error}
                submitting={loading}
                submitLabel="Register Candidate"
                submittingLabel="Registering..."
                onChange={handleChange}
                onCancel={() => navigate('/candidates')}
                onSubmit={handleSubmit}
            />
        </div>
    );
};

export default CreateCandidateScreen;
