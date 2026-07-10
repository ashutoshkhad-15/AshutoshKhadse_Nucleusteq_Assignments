/**
 * Render the interview feedback form.
 */
const FeedbackForm = ({
    values,
    validationErrors,
    formError,
    submitting,
    disabled,
    submitLabel,
    submittingLabel,
    onChange,
    onCancel,
    onSubmit,
}) => (
    <div className="form-card">
        {formError ? <div className="error-banner">{formError}</div> : null}
        <form onSubmit={onSubmit} noValidate>
            <h2 className="form-section-title">Submit Feedback</h2>
            <div className="form-grid">
                {[
                    { key: 'technicalRating', label: 'Technical Rating' },
                    { key: 'communicationRating', label: 'Communication Rating' },
                    { key: 'problemSolving', label: 'Problem Solving' },
                ].map((field) => (
                    <div key={field.key} className="form-group">
                        <label className="form-label" htmlFor={field.key}>{field.label} *</label>
                        <select id={field.key} className={`form-control ${validationErrors[field.key] ? 'form-control-error' : ''}`} value={values[field.key]} onChange={(e) => onChange(field.key, e.target.value)}>
                            <option value="">Select rating</option>
                            {Array.from({ length: 5 }).map((_, index) => <option key={index + 1} value={index + 1}>{index + 1}</option>)}
                        </select>
                        {validationErrors[field.key] ? <p className="field-error">{validationErrors[field.key]}</p> : null}
                    </div>
                ))}
                <div className="form-group form-group-full">
                    <label className="form-label" htmlFor="techAreasCovered">Tech Areas Covered *</label>
                    <input id="techAreasCovered" className={`form-control ${validationErrors.techAreasCovered ? 'form-control-error' : ''}`} value={values.techAreasCovered} onChange={(e) => onChange('techAreasCovered', e.target.value)} placeholder="Enter areas separated by commas" />
                    {validationErrors.techAreasCovered ? <p className="field-error">{validationErrors.techAreasCovered}</p> : null}
                </div>
                <div className="form-group form-group-full">
                    <label className="form-label" htmlFor="comments">Comments *</label>
                    <textarea id="comments" rows={6} className={`form-control form-textarea ${validationErrors.comments ? 'form-control-error' : ''}`} value={values.comments} onChange={(e) => onChange('comments', e.target.value)} />
                    {validationErrors.comments ? <p className="field-error">{validationErrors.comments}</p> : null}
                </div>
                <div className="form-group form-group-full">
                    <label className="form-label" htmlFor="recommendation">Recommendation *</label>
                    <select id="recommendation" className={`form-control ${validationErrors.recommendation ? 'form-control-error' : ''}`} value={values.recommendation} onChange={(e) => onChange('recommendation', e.target.value)}>
                        <option value="">Select recommendation</option>
                        <option value="NEXT_ROUND">NEXT_ROUND</option>
                        <option value="SELECT">SELECT</option>
                        <option value="REJECT">REJECT</option>
                    </select>
                    {validationErrors.recommendation ? <p className="field-error">{validationErrors.recommendation}</p> : null}
                </div>
            </div>
            <div className="form-actions">
                <button type="button" onClick={onCancel} className="btn-secondary" disabled={submitting}>Cancel</button>
                <button type="submit" disabled={submitting || disabled} className="btn-primary">{submitting ? submittingLabel : submitLabel}</button>
            </div>
        </form>
    </div>
);

export default FeedbackForm;
