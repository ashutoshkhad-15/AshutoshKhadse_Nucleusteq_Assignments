import { CircleCheckBig } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import JobForm from '../components/jobs/JobForm';
import JobPageHeader from '../components/jobs/JobPageHeader';
import { jobService } from '../services/jobService';
import {
    buildJobPayload,
    getJobManagementErrorMessage,
    JOB_FORM_DEFAULTS,
    mapJobToFormValues,
    useJobFormState,
} from '../utils/jobManagement';
import useJobFormSubmission from '../hooks/useJobFormSubmission';
import '../styles/job-management.css';

/**
 * Render the edit-job workflow with existing values prefilled from the API.
 *
 * @returns {JSX.Element} Edit job screen.
 */
const EditJobScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);
    const {
        currentErrors,
        handleFieldChange,
        addSkill,
        removeSkill,
        setValidationErrors,
        setValues,
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

    useEffect(() => {
        /**
         * Load the selected job and prefill the edit form.
         *
         * @returns {Promise<void>}
         */
        const controller = new AbortController();
        const timeoutId = window.setTimeout(async () => {
            try {
                setLoading(true);
                const job = await jobService.getJobById(id, { signal: controller.signal });
                setValues(mapJobToFormValues(job));
                setError(null);
            } catch (err) {
                if (err?.name === 'CanceledError') {
                    return;
                }
                setError(getJobManagementErrorMessage(err, 'Failed to load job details.'));
            } finally {
                if (!controller.signal.aborted) {
                    setLoading(false);
                }
            }
        }, 20);

        return () => {
            window.clearTimeout(timeoutId);
            controller.abort();
        };
    }, [id, setValues]);

    const { handleSubmit } = useJobFormSubmission({
        getValidationErrors: () => currentErrors,
        setValidationErrors,
        setFormError: setError,
        onSubmitValid: async () => {
            setSaving(true);
            try {
                const payload = buildJobPayload(values);
                await jobService.updateJob(id, payload);
                navigate('/jobs', {
                    replace: true,
                    state: { successMessage: `Job "${payload.jobTitle}" updated successfully.` },
                });
            } catch (err) {
                setError(getJobManagementErrorMessage(err, 'Failed to update job.'));
            } finally {
                setSaving(false);
            }
        },
    });

    if (loading) {
        return <div className="um-state">Loading job details...</div>;
    }

    return (
        <div className="um-container um-form-page">
            <JobPageHeader
                eyebrow="Hiring"
                title="Edit Job"
                description="Update responsibilities, required skills, and hiring requirements for this role."
                actions={(
                    <span className="jm-header-pill">
                        <CircleCheckBig size={16} aria-hidden="true" />
                        Change Management
                    </span>
                )}
            />

            <JobForm
                values={values}
                validationErrors={validationErrors}
                formError={error}
                submitting={saving}
                submitLabel="Save Changes"
                submittingLabel="Saving..."
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

export default EditJobScreen;
