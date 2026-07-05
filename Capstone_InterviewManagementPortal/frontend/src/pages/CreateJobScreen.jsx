import { Plus } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import JobForm from '../components/jobs/JobForm';
import JobPageHeader from '../components/jobs/JobPageHeader';
import { jobService } from '../services/jobService';
import { buildJobPayload, getJobManagementErrorMessage, JOB_FORM_DEFAULTS, useJobFormState } from '../utils/jobManagement';
import useJobFormSubmission from '../hooks/useJobFormSubmission';
import '../styles/job-management.css';

/**
 * Render the create-job workflow with inline validation and chip-based skills input.
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
        addSkill,
        removeSkill,
        setValidationErrors,
        validationErrors,
        values,
    } = useJobFormState(JOB_FORM_DEFAULTS);
    const [skillDraft, setSkillDraft] = useState('');

    const handleAddSkill = () => {
        const message = addSkill(skillDraft);
        if (message) {
            setValidationErrors((current) => ({ ...current, requiredSkills: message }));
            return;
        }
        setSkillDraft('');
    };

    const { handleSubmit } = useJobFormSubmission({
        getValidationErrors: () => currentErrors,
        setValidationErrors,
        setFormError: setError,
        onSubmitValid: async () => {
            setLoading(true);
            try {
                const payload = buildJobPayload(values);
                await jobService.createJob(payload);
                navigate('/jobs', {
                    replace: true,
                    state: { successMessage: `Job "${payload.jobTitle}" created successfully.` },
                });
            } catch (err) {
                setError(getJobManagementErrorMessage(err, 'Failed to create job. Please try again.'));
            } finally {
                setLoading(false);
            }
        },
    });

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
                submitLabel="Create Job"
                submittingLabel="Creating..."
                onChange={handleFieldChange}
                onCancel={() => navigate('/jobs')}
                onSubmit={handleSubmit}
                onAddSkill={handleAddSkill}
                onRemoveSkill={removeSkill}
                skillDraft={skillDraft}
                setSkillDraft={setSkillDraft}
            />
        </div>
    );
};

export default CreateJobScreen;
