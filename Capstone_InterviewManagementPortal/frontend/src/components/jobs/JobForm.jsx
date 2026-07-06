import { EMPLOYMENT_TYPE_OPTIONS } from '../../utils/jobManagement';

/**
 * Renders the job create and edit form.
 */
const JobForm = ({ values, validationErrors, formError, submitting, submitLabel, submittingLabel, onChange, onCancel, onSubmit, onAddSkill, onRemoveSkill, skillDraft, setSkillDraft }) => (
    <div className="form-card">
        {formError ? <div className="error-banner">{formError}</div> : null}
        <form onSubmit={onSubmit} noValidate>
            <h2 className="form-section-title">Job Details</h2>
            <div className="form-grid">
                <div className="form-group">
                    <label className="form-label" htmlFor="jobTitle">Job Title *</label>
                    <input id="jobTitle" className={`form-control ${validationErrors.jobTitle ? 'form-control-error' : ''}`} value={values.jobTitle} onChange={(e) => onChange('jobTitle', e.target.value)} />
                    {validationErrors.jobTitle ? <p className="field-error">{validationErrors.jobTitle}</p> : null}
                </div>
                <div className="form-group">
                    <label className="form-label" htmlFor="jobRole">Job Role *</label>
                    <input id="jobRole" className={`form-control ${validationErrors.jobRole ? 'form-control-error' : ''}`} value={values.jobRole} onChange={(e) => onChange('jobRole', e.target.value)} />
                    {validationErrors.jobRole ? <p className="field-error">{validationErrors.jobRole}</p> : null}
                </div>
                <div className="form-group">
                    <label className="form-label" htmlFor="experienceRequired">Experience Required *</label>
                    <input id="experienceRequired" className={`form-control ${validationErrors.experienceRequired ? 'form-control-error' : ''}`} value={values.experienceRequired} onChange={(e) => onChange('experienceRequired', e.target.value)} />
                    {validationErrors.experienceRequired ? <p className="field-error">{validationErrors.experienceRequired}</p> : null}
                </div>
                <div className="form-group">
                    <label className="form-label" htmlFor="employmentType">Employment Type *</label>
                    <select id="employmentType" className={`form-control ${validationErrors.employmentType ? 'form-control-error' : ''}`} value={values.employmentType} onChange={(e) => onChange('employmentType', e.target.value)}>
                        <option value="">Select employment type</option>
                        {EMPLOYMENT_TYPE_OPTIONS.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
                    </select>
                    {validationErrors.employmentType ? <p className="field-error">{validationErrors.employmentType}</p> : null}
                </div>
                <div className="form-group form-group-full">
                    <label className="form-label" htmlFor="jobDetails">Job Details *</label>
                    <textarea id="jobDetails" rows={7} className={`form-control form-textarea ${validationErrors.jobDetails ? 'form-control-error' : ''}`} value={values.jobDetails} onChange={(e) => onChange('jobDetails', e.target.value)} />
                    {validationErrors.jobDetails ? <p className="field-error">{validationErrors.jobDetails}</p> : null}
                </div>
                <div className="form-group form-group-full">
                    <label className="form-label" htmlFor="skillDraft">Required Skills *</label>
                    <div className="jm-skill-input-row">
                        <input id="skillDraft" className={`form-control ${validationErrors.requiredSkills ? 'form-control-error' : ''}`} value={skillDraft} onChange={(e) => setSkillDraft(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); onAddSkill(); } }} />
                        <button type="button" className="btn-secondary" onClick={onAddSkill}>Add</button>
                    </div>
                    <div className="jm-skill-list">
                        {values.requiredSkills.map((skill) => (
                            <span key={skill} className="jm-skill-pill">
                                {skill}
                                <button type="button" className="jm-skill-remove" onClick={() => onRemoveSkill(skill)}>Remove</button>
                            </span>
                        ))}
                    </div>
                    {validationErrors.requiredSkills ? <p className="field-error">{validationErrors.requiredSkills}</p> : null}
                </div>
                <div className="form-group form-group-full">
                    <label className="form-label" htmlFor="location">Location *</label>
                    <input id="location" className={`form-control ${validationErrors.location ? 'form-control-error' : ''}`} value={values.location} onChange={(e) => onChange('location', e.target.value)} />
                    {validationErrors.location ? <p className="field-error">{validationErrors.location}</p> : null}
                </div>
            </div>
            <div className="form-actions">
                <button type="button" onClick={onCancel} className="btn-secondary" disabled={submitting}>Cancel</button>
                <button type="submit" disabled={submitting} className="btn-primary">{submitting ? submittingLabel : submitLabel}</button>
            </div>
        </form>
    </div>
);

export default JobForm;
