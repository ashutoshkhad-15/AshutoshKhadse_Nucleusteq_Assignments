import { Plus } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import JobForm from '../components/jobs/JobForm';
import JobPageHeader from '../components/jobs/JobPageHeader';
import { jobService } from '../services/jobService';
import {
    buildJobPayload,
    getJobManagementErrorMessage,
    JOB_FORM_DEFAULTS,
    useJobFormState,
} from '../utils/jobManagement';
import '../styles/job-management.css';

/**
 * Render the HR workflow for creating a new job description.
 *
 * @returns {JSX.Element} Create job screen.
 */
const CreateJobScreen = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const {
        currentErrors,
        handleFieldChange,
        setValidationErrors,
        validationErrors,
        values,
    } = useJobFormState(JOB_FORM_DEFAULTS);

    /**
     * Create a job after client-side validation passes.
     *
     * @param {React.FormEvent<HTMLFormElement>} event - Form submission event.
     * @returns {Promise<void>}
     */
    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);

        if (Object.keys(currentErrors).length > 0) {
            setValidationErrors(currentErrors);
            return;
        }

        try {
            setLoading(true);
            setValidationErrors({});
            const payload = buildJobPayload(values);
            await jobService.createJob(payload);
            navigate('/jobs', {
                replace: true,
                state: { successMessage: `Job "${payload.title}" created successfully.` },
            });
        } catch (err) {
            setError(getJobManagementErrorMessage(err, 'Failed to create job. Please try again.'));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="um-container um-form-page">
            <JobPageHeader
                eyebrow="Hiring"
                title="Create Job"
                description="Publish a complete job description so recruiters and interviewers work from the same brief."
                actions={(
                    <span className="jm-header-pill">
                        <Plus size={16} aria-hidden="true" />
                        New Opening
                    </span>
                )}
            />

            <JobForm
                values={values}
                validationErrors={validationErrors}
                formError={error}
                submitting={loading}
                submitDisabled={loading || Object.keys(currentErrors).length > 0}
                showStatusToggle={false}
                isActive
                submitLabel="Create Job"
                submittingLabel="Creating..."
                onChange={handleFieldChange}
                onActiveChange={() => {}}
                onCancel={() => navigate('/jobs')}
                onSubmit={handleSubmit}
            />
        </div>
    );
};

export default CreateJobScreen;
