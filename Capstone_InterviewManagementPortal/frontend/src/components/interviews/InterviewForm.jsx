/**
 * Render the interview schedule form.
 */
const InterviewForm = ({
    values,
    validationErrors,
    formError,
    submitting,
    disabled,
    submitLabel,
    submittingLabel,
    candidateOptions,
    jobOptions,
    interviewerOptions,
    onChange,
    onCancel,
    onSubmit,
    onAddFocusArea,
    onRemoveFocusArea,
    focusAreaDraft,
    setFocusAreaDraft,
}) => (
    <div className="form-card">
        {formError ? <div className="error-banner">{formError}</div> : null}
        <form onSubmit={onSubmit} noValidate>
            <h2 className="form-section-title">Schedule Interview</h2>
            <div className="form-grid">
                <div className="form-group">
                    <label className="form-label" htmlFor="candidateId">Candidate *</label>
                    <select id="candidateId" className={`form-control ${validationErrors.candidateId ? 'form-control-error' : ''}`} value={values.candidateId} onChange={(e) => onChange('candidateId', e.target.value)} disabled={disabled}>
                        <option value="">Select candidate</option>
                        {candidateOptions.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
                    </select>
                    {validationErrors.candidateId ? <p className="field-error">{validationErrors.candidateId}</p> : null}
                </div>
                <div className="form-group">
                    <label className="form-label" htmlFor="jobId">Job Title *</label>
                    <select id="jobId" className={`form-control ${validationErrors.jobId ? 'form-control-error' : ''}`} value={values.jobId} onChange={(e) => onChange('jobId', e.target.value)} disabled={disabled}>
                        <option value="">Select job</option>
                        {jobOptions.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
                    </select>
                    {validationErrors.jobId ? <p className="field-error">{validationErrors.jobId}</p> : null}
                </div>
                <div className="form-group">
                    <label className="form-label" htmlFor="interviewDate">Interview Date *</label>
                    <input id="interviewDate" type="date" className={`form-control ${validationErrors.interviewDate ? 'form-control-error' : ''}`} value={values.interviewDate} onChange={(e) => onChange('interviewDate', e.target.value)} disabled={disabled} />
                    {validationErrors.interviewDate ? <p className="field-error">{validationErrors.interviewDate}</p> : null}
                </div>
                <div className="form-group">
                    <label className="form-label" htmlFor="interviewTime">Interview Time *</label>
                    <input id="interviewTime" type="time" className={`form-control ${validationErrors.interviewTime ? 'form-control-error' : ''}`} value={values.interviewTime} onChange={(e) => onChange('interviewTime', e.target.value)} disabled={disabled} />
                    {validationErrors.interviewTime ? <p className="field-error">{validationErrors.interviewTime}</p> : null}
                </div>
                <div className="form-group form-group-full">
                    <label className="form-label" htmlFor="interviewerId">Assigned Interviewer *</label>
                    <select id="interviewerId" className={`form-control ${validationErrors.interviewerId ? 'form-control-error' : ''}`} value={values.interviewerId} onChange={(e) => onChange('interviewerId', e.target.value)} disabled={disabled}>
                        <option value="">Select interviewer</option>
                        {interviewerOptions.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
                    </select>
                    {validationErrors.interviewerId ? <p className="field-error">{validationErrors.interviewerId}</p> : null}
                </div>
                <div className="form-group form-group-full">
                    <label className="form-label" htmlFor="focusAreaDraft">Focus Tech Areas *</label>
                    <div className="jm-skill-input-row">
                        <input id="focusAreaDraft" className={`form-control ${validationErrors.focusTechAreas ? 'form-control-error' : ''}`} value={focusAreaDraft} onChange={(e) => setFocusAreaDraft(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); onAddFocusArea(); } }} disabled={disabled} />
                        <button type="button" className="btn-secondary" onClick={onAddFocusArea} disabled={disabled}>Add</button>
                    </div>
                    <div className="jm-skill-list">
                        {values.focusTechAreas.map((area) => (
                            <span key={area} className="jm-skill-pill">
                                {area}
                                <button type="button" className="jm-skill-remove" onClick={() => onRemoveFocusArea(area)} disabled={disabled}>Remove</button>
                            </span>
                        ))}
                    </div>
                    {validationErrors.focusTechAreas ? <p className="field-error">{validationErrors.focusTechAreas}</p> : null}
                </div>
            </div>
            <div className="form-actions">
                <button type="button" onClick={onCancel} className="btn-secondary" disabled={submitting}>Cancel</button>
                <button type="submit" disabled={submitting || disabled} className="btn-primary">{submitting ? submittingLabel : submitLabel}</button>
            </div>
        </form>
    </div>
);

export default InterviewForm;
