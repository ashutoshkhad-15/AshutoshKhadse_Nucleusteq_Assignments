import AppliedJobSelect from './AppliedJobSelect';

/** Render the shared create/edit candidate form fields and actions. */
const CandidateForm = ({
    values,
    validationErrors,
    formError,
    submitting,
    submitLabel,
    submittingLabel,
    onChange,
    onCancel,
    onSubmit,
    selectedAppliedJob,
}) => (
    <div className="form-card">
        {formError ? <div className="error-banner">{formError}</div> : null}
        <form onSubmit={onSubmit} noValidate>
            <div className="form-section">
                <div className="form-section-header">
                    <h2 className="form-section-title">Candidate Details</h2>
                    <p className="form-section-copy">Capture the candidate profile needed for interview tracking.</p>
                </div>
                <div className="form-grid">
                    <div className="form-group">
                        <label className="form-label" htmlFor="candidate-first-name">First Name <span className="required-indicator">*</span></label>
                        <input id="candidate-first-name" value={values.firstName} onChange={(e) => onChange('firstName', e.target.value)} className={`form-control ${validationErrors.firstName ? 'form-control-error' : ''}`} />
                        {validationErrors.firstName ? <p className="field-error">{validationErrors.firstName}</p> : null}
                    </div>
                    <div className="form-group">
                        <label className="form-label" htmlFor="candidate-last-name">Last Name <span className="required-indicator">*</span></label>
                        <input id="candidate-last-name" value={values.lastName} onChange={(e) => onChange('lastName', e.target.value)} className={`form-control ${validationErrors.lastName ? 'form-control-error' : ''}`} />
                        {validationErrors.lastName ? <p className="field-error">{validationErrors.lastName}</p> : null}
                    </div>
                    <div className="form-group">
                        <label className="form-label" htmlFor="candidate-email">Email Address <span className="required-indicator">*</span></label>
                        <input id="candidate-email" type="email" value={values.email} onChange={(e) => onChange('email', e.target.value)} className={`form-control ${validationErrors.email ? 'form-control-error' : ''}`} />
                        {validationErrors.email ? <p className="field-error">{validationErrors.email}</p> : null}
                    </div>
                    <div className="form-group">
                        <label className="form-label" htmlFor="candidate-mobile">Mobile Number <span className="required-indicator">*</span></label>
                        <input id="candidate-mobile" type="tel" inputMode="numeric" maxLength={10} value={values.mobile} onChange={(e) => onChange('mobile', e.target.value)} className={`form-control ${validationErrors.mobile ? 'form-control-error' : ''}`} />
                        {validationErrors.mobile ? <p className="field-error">{validationErrors.mobile}</p> : null}
                    </div>
                    <div className="form-group">
                        <label className="form-label" htmlFor="candidate-company">Current Company <span className="required-indicator">*</span></label>
                        <input id="candidate-company" value={values.currentCompany} onChange={(e) => onChange('currentCompany', e.target.value)} className={`form-control ${validationErrors.currentCompany ? 'form-control-error' : ''}`} />
                        {validationErrors.currentCompany ? <p className="field-error">{validationErrors.currentCompany}</p> : null}
                    </div>
                    <div className="form-group">
                        <label className="form-label" htmlFor="candidate-experience">Total Experience <span className="required-indicator">*</span></label>
                        <input id="candidate-experience" value={values.totalExperience} onChange={(e) => onChange('totalExperience', e.target.value)} className={`form-control ${validationErrors.totalExperience ? 'form-control-error' : ''}`} placeholder='e.g. "2 years" or "5-7 years"' />
                        {validationErrors.totalExperience ? <p className="field-error">{validationErrors.totalExperience}</p> : null}
                    </div>
                    <div className="form-group form-group-full">
                        <label className="form-label" htmlFor="candidate-applied-job">Applied Job <span className="required-indicator">*</span></label>
                        <AppliedJobSelect
                            value={values.appliedJobId}
                            onChange={(jobId, job) => onChange('appliedJobId', jobId, job)}
                            error={validationErrors.appliedJobId}
                            initialJob={selectedAppliedJob}
                        />
                        {validationErrors.appliedJobId ? <p className="field-error">{validationErrors.appliedJobId}</p> : null}
                    </div>
                </div>
            </div>
            <div className="form-actions">
                <button type="button" onClick={onCancel} className="btn-secondary" disabled={submitting}>Cancel</button>
                <button type="submit" disabled={submitting} className="btn-primary">{submitting ? submittingLabel : submitLabel}</button>
            </div>
        </form>
    </div>
);

export default CandidateForm;
