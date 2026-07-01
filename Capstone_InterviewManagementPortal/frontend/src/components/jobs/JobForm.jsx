import { ArrowLeft, Save } from 'lucide-react';
import JobStatusBadge from './JobStatusBadge';

/**
 * Render the shared create and edit job form fields and actions.
 *
 * @param {object} props - Component props.
 * @param {object} props.values - Current form values.
 * @param {object} props.validationErrors - Field validation errors.
 * @param {string | null} props.formError - Form-level error message.
 * @param {boolean} props.submitting - Whether the form is being submitted.
 * @param {boolean} props.submitDisabled - Whether submit should be disabled.
 * @param {boolean} props.showStatusToggle - Whether to render the active status switch.
 * @param {boolean} props.isActive - Current job status.
 * @param {string} props.submitLabel - Idle submit button label.
 * @param {string} props.submittingLabel - Busy submit button label.
 * @param {(field: string, value: string) => void} props.onChange - Field update callback.
 * @param {(value: boolean) => void} props.onActiveChange - Status toggle callback.
 * @param {() => void} props.onCancel - Cancel action.
 * @param {(event: React.FormEvent<HTMLFormElement>) => void} props.onSubmit - Submit handler.
 * @returns {JSX.Element} Shared job form UI.
 */
const JobForm = ({
    values,
    validationErrors,
    formError,
    submitting,
    submitDisabled,
    showStatusToggle,
    isActive,
    submitLabel,
    submittingLabel,
    onChange,
    onActiveChange,
    onCancel,
    onSubmit,
}) => (
    <div className="form-card">
        {formError ? <div className="error-banner">{formError}</div> : null}

        <form onSubmit={onSubmit} noValidate>
            <div className="form-section">
                <div className="form-section-header">
                    <h2 className="form-section-title">Job Details</h2>
                    <p className="form-section-copy">Capture a complete and searchable job description for the hiring team.</p>
                </div>

                <div className="form-grid">
                    <div className="form-group">
                        <label className="form-label" htmlFor="job-title">
                            Job Title <span className="required-indicator">*</span>
                        </label>
                        <input
                            id="job-title"
                            type="text"
                            value={values.title}
                            onChange={(event) => onChange('title', event.target.value)}
                            className={`form-control ${validationErrors.title ? 'form-control-error' : ''}`}
                            placeholder="Senior Data Engineer"
                            maxLength={100}
                            aria-invalid={Boolean(validationErrors.title)}
                            aria-describedby={validationErrors.title ? 'job-title-error' : undefined}
                        />
                        {validationErrors.title ? <p id="job-title-error" className="field-error">{validationErrors.title}</p> : null}
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="job-department">
                            Department <span className="required-indicator">*</span>
                        </label>
                        <input
                            id="job-department"
                            type="text"
                            value={values.department}
                            onChange={(event) => onChange('department', event.target.value)}
                            className={`form-control ${validationErrors.department ? 'form-control-error' : ''}`}
                            placeholder="Data Platform"
                            maxLength={50}
                            aria-invalid={Boolean(validationErrors.department)}
                            aria-describedby={validationErrors.department ? 'job-department-error' : undefined}
                        />
                        {validationErrors.department ? <p id="job-department-error" className="field-error">{validationErrors.department}</p> : null}
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="job-experience">
                            Experience Required <span className="required-indicator">*</span>
                        </label>
                        <input
                            id="job-experience"
                            type="text"
                            value={values.experience_required}
                            onChange={(event) => onChange('experience_required', event.target.value)}
                            className={`form-control ${validationErrors.experience_required ? 'form-control-error' : ''}`}
                            placeholder="2-4 years"
                            maxLength={60}
                            aria-invalid={Boolean(validationErrors.experience_required)}
                            aria-describedby={validationErrors.experience_required ? 'job-experience-error' : undefined}
                        />
                        {validationErrors.experience_required ? <p id="job-experience-error" className="field-error">{validationErrors.experience_required}</p> : null}
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="job-location">
                            Location <span className="required-indicator">*</span>
                        </label>
                        <input
                            id="job-location"
                            type="text"
                            value={values.location}
                            onChange={(event) => onChange('location', event.target.value)}
                            className={`form-control ${validationErrors.location ? 'form-control-error' : ''}`}
                            placeholder="Indore, MP or Remote"
                            maxLength={80}
                            aria-invalid={Boolean(validationErrors.location)}
                            aria-describedby={validationErrors.location ? 'job-location-error' : undefined}
                        />
                        {validationErrors.location ? <p id="job-location-error" className="field-error">{validationErrors.location}</p> : null}
                    </div>

                    <div className="form-group form-group-full">
                        <label className="form-label" htmlFor="job-skills">
                            Required Skills <span className="required-indicator">*</span>
                        </label>
                        <textarea
                            id="job-skills"
                            value={values.skills}
                            onChange={(event) => onChange('skills', event.target.value)}
                            className={`form-control form-textarea ${validationErrors.skills ? 'form-control-error' : ''}`}
                            placeholder="Python, SQL, FastAPI"
                            rows={4}
                            aria-invalid={Boolean(validationErrors.skills)}
                            aria-describedby={validationErrors.skills ? 'job-skills-error' : 'job-skills-helper'}
                        />
                        {validationErrors.skills ? <p id="job-skills-error" className="field-error">{validationErrors.skills}</p> : null}
                        <p id="job-skills-helper" className="field-helper">Separate skills with commas or new lines. Duplicate entries are removed automatically.</p>
                    </div>

                    <div className="form-group form-group-full">
                        <label className="form-label" htmlFor="job-description">
                            Description <span className="required-indicator">*</span>
                        </label>
                        <textarea
                            id="job-description"
                            value={values.description}
                            onChange={(event) => onChange('description', event.target.value)}
                            className={`form-control form-textarea form-textarea-lg ${validationErrors.description ? 'form-control-error' : ''}`}
                            placeholder="Describe responsibilities, expectations, and the impact of the role."
                            rows={8}
                            aria-invalid={Boolean(validationErrors.description)}
                            aria-describedby={validationErrors.description ? 'job-description-error' : undefined}
                        />
                        {validationErrors.description ? <p id="job-description-error" className="field-error">{validationErrors.description}</p> : null}
                    </div>

                    {showStatusToggle ? (
                        <div className="form-group form-group-full">
                            <div className="jm-status-toggle">
                                <div>
                                    <p className="jm-status-title">Posting Status</p>
                                    <p className="field-helper">Close the role to hide it from active hiring workflows without deleting the description.</p>
                                </div>
                                <label className="jm-switch" htmlFor="job-active-toggle">
                                    <input
                                        id="job-active-toggle"
                                        type="checkbox"
                                        checked={isActive}
                                        onChange={(event) => onActiveChange(event.target.checked)}
                                    />
                                    <span className="jm-switch-track">
                                        <span className="jm-switch-thumb" />
                                    </span>
                                    <JobStatusBadge isActive={isActive} />
                                </label>
                            </div>
                        </div>
                    ) : null}
                </div>
            </div>

            <div className="form-actions">
                <button type="button" onClick={onCancel} className="btn-secondary jm-button-with-icon" disabled={submitting}>
                    <ArrowLeft size={16} aria-hidden="true" />
                    Cancel
                </button>
                <button type="submit" disabled={submitDisabled || submitting} className="btn-primary jm-button-with-icon">
                    <Save size={16} aria-hidden="true" />
                    {submitting ? submittingLabel : submitLabel}
                </button>
            </div>
        </form>
    </div>
);

export default JobForm;
