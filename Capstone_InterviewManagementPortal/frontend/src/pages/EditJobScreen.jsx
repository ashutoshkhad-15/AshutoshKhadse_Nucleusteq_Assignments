import { CircleCheckBig } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
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
import '../styles/job-management.css';

/**
 * Render the HR workflow for editing an existing job description.
 *
 * @returns {JSX.Element} Edit job screen.
 */
const EditJobScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [isActive, setIsActive] = useState(true);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);
    const submittingRef = useRef(false);
    const {
        currentErrors,
        handleFieldChange,
        setValidationErrors,
        setValues,
        validationErrors,
        values,
    } = useJobFormState(JOB_FORM_DEFAULTS);

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
                setIsActive(Boolean(job.is_active));
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

    /**
     * Persist job changes after validation succeeds.
     *
     * @param {React.FormEvent<HTMLFormElement>} event - Form submission event.
     * @returns {Promise<void>}
     */
    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);

        if (submittingRef.current) {
            return;
        }

        if (Object.keys(currentErrors).length > 0) {
            setValidationErrors(currentErrors);
            return;
        }

        try {
            submittingRef.current = true;
            setSaving(true);
            setValidationErrors({});
            const payload = {
                ...buildJobPayload(values),
                is_active: isActive,
            };
            await jobService.updateJob(id, payload);
            navigate('/jobs', {
                replace: true,
                state: { successMessage: `Job "${payload.title}" updated successfully.` },
            });
        } catch (err) {
            setError(getJobManagementErrorMessage(err, 'Failed to update job.'));
        } finally {
            submittingRef.current = false;
            setSaving(false);
        }
    };

    if (loading) {
        return <div className="um-state">Loading job details...</div>;
    }

    return (
        <div className="um-container um-form-page">
            <JobPageHeader
                eyebrow="Hiring"
                title="Edit Job"
                description="Update responsibilities, required skills, and posting status for this role."
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
                submitDisabled={saving || Object.keys(currentErrors).length > 0}
                showStatusToggle
                isActive={isActive}
                submitLabel="Save Changes"
                submittingLabel="Saving..."
                onChange={handleFieldChange}
                onActiveChange={setIsActive}
                onCancel={() => navigate('/jobs')}
                onSubmit={handleSubmit}
            />
        </div>
    );
};

export default EditJobScreen;
