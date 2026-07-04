import { ArrowLeft, Plus, Save, X } from 'lucide-react';
import { EMPLOYMENT_TYPE_OPTIONS } from '../../utils/jobManagement';

const JobForm = ({ values, validationErrors, formError, submitting, submitLabel, submittingLabel, onChange, onCancel, onSubmit, onAddSkill, onRemoveSkill, skillDraft, setSkillDraft }) => (
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
                        <label className="form-label" htmlFor="jobTitle">Job Title <span className="required-indicator">*</span></label>
                        <input id="jobTitle" className={`form-control ${validationErrors.jobTitle ? 'form-control-error' : ''}`} value={values.jobTitle} onChange={(e) => onChange('jobTitle', e.target.value)} placeholder="Senior Python Developer" aria-invalid={Boolean(validationErrors.jobTitle)} aria-describedby={validationErrors.jobTitle ? 'job-title-error' : undefined} />
                        {validationErrors.jobTitle ? <p id="job-title-error" className="field-error">{validationErrors.jobTitle}</p> : null}
                    </div>
                    <div className="form-group">
                        <label className="form-label" htmlFor="jobRole">Job Role <span className="required-indicator">*</span></label>
                        <input id="jobRole" className={`form-control ${validationErrors.jobRole ? 'form-control-error' : ''}`} value={values.jobRole} onChange={(e) => onChange('jobRole', e.target.value)} placeholder="Backend Developer" aria-invalid={Boolean(validationErrors.jobRole)} aria-describedby={validationErrors.jobRole ? 'job-role-error' : undefined} />
                        {validationErrors.jobRole ? <p id="job-role-error" className="field-error">{validationErrors.jobRole}</p> : null}
                    </div>
                    <div className="form-group">
                        <label className="form-label" htmlFor="experienceRequired">Experience Required <span className="required-indicator">*</span></label>
                        <input id="experienceRequired" className={`form-control ${validationErrors.experienceRequired ? 'form-control-error' : ''}`} value={values.experienceRequired} onChange={(e) => onChange('experienceRequired', e.target.value)} placeholder='e.g. 3+ years' aria-invalid={Boolean(validationErrors.experienceRequired)} aria-describedby={validationErrors.experienceRequired ? 'job-experience-error' : undefined} />
                        {validationErrors.experienceRequired ? <p id="job-experience-error" className="field-error">{validationErrors.experienceRequired}</p> : null}
                    </div>
                    <div className="form-group">
                        <label className="form-label" htmlFor="employmentType">Employment Type <span className="required-indicator">*</span></label>
                        <select id="employmentType" className={`form-control ${validationErrors.employmentType ? 'form-control-error' : ''}`} value={values.employmentType} onChange={(e) => onChange('employmentType', e.target.value)} aria-invalid={Boolean(validationErrors.employmentType)} aria-describedby={validationErrors.employmentType ? 'job-employment-error' : undefined}>
                            <option value="">Select employment type</option>
                            {EMPLOYMENT_TYPE_OPTIONS.map((opt) => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
                        </select>
                        {validationErrors.employmentType ? <p id="job-employment-error" className="field-error">{validationErrors.employmentType}</p> : null}
                    </div>
                    <div className="form-group form-group-full">
                        <label className="form-label" htmlFor="jobDetails">Job Details <span className="required-indicator">*</span></label>
                        <textarea id="jobDetails" rows={7} className={`form-control form-textarea ${validationErrors.jobDetails ? 'form-control-error' : ''}`} value={values.jobDetails} onChange={(e) => onChange('jobDetails', e.target.value)} placeholder="Describe the responsibilities, scope, and success outcomes." aria-invalid={Boolean(validationErrors.jobDetails)} aria-describedby={validationErrors.jobDetails ? 'job-details-error' : undefined} />
                        {validationErrors.jobDetails ? <p id="job-details-error" className="field-error">{validationErrors.jobDetails}</p> : null}
                    </div>
                    <div className="form-group form-group-full">
                        <label className="form-label" htmlFor="skillDraft">Required Skills <span className="required-indicator">*</span></label>
                        <div className="jm-skill-input-row">
                            <input id="skillDraft" className={`form-control ${validationErrors.requiredSkills ? 'form-control-error' : ''}`} value={skillDraft} onChange={(e) => setSkillDraft(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); onAddSkill(); } }} placeholder="Type a skill and press Enter" aria-invalid={Boolean(validationErrors.requiredSkills)} aria-describedby={validationErrors.requiredSkills ? 'job-skills-error' : undefined} />
                            <button type="button" className="btn-secondary jm-button-with-icon" onClick={onAddSkill}><Plus size={14} aria-hidden="true" />Add</button>
                        </div>
                        <div className="jm-skill-list">
                            {values.requiredSkills.map((skill) => (
                                <span key={skill} className="jm-skill-pill">
                                    {skill}
                                    <button type="button" className="jm-skill-remove" onClick={() => onRemoveSkill(skill)} aria-label={`Remove skill ${skill}`}>
                                        <X size={12} />
                                    </button>
                                </span>
                            ))}
                        </div>
                        {validationErrors.requiredSkills ? <p id="job-skills-error" className="field-error">{validationErrors.requiredSkills}</p> : null}
                    </div>
                    <div className="form-group form-group-full">
                        <label className="form-label" htmlFor="location">Location <span className="required-indicator">*</span></label>
                        <input id="location" className={`form-control ${validationErrors.location ? 'form-control-error' : ''}`} value={values.location} onChange={(e) => onChange('location', e.target.value)} placeholder="Indore, Madhya Pradesh" aria-invalid={Boolean(validationErrors.location)} aria-describedby={validationErrors.location ? 'job-location-error' : undefined} />
                        {validationErrors.location ? <p id="job-location-error" className="field-error">{validationErrors.location}</p> : null}
                    </div>
                </div>
            </div>
            <div className="form-actions">
                <button type="button" onClick={onCancel} className="btn-secondary jm-button-with-icon" disabled={submitting}><ArrowLeft size={16} />Cancel</button>
                <button type="submit" disabled={submitting} className="btn-primary jm-button-with-icon"><Save size={16} />{submitting ? submittingLabel : submitLabel}</button>
            </div>
        </form>
    </div>
);

export default JobForm;
