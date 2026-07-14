import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { USER_ROLES } from '../constants/roles';
import { ROUTES } from '../constants/routes';
import '../styles/interview-management.css';
import { formatInterviewDate, getInterviewManagementErrorMessage } from '../utils/interviewManagement';
import { loadInterviewDetails } from '../utils/pageLoaders';
import { getStoredUserRole, isInterviewer } from '../utils/session';

/**
 * Render the read-only interview details screen.
 */
const InterviewDetailsScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [interview, setInterview] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const role = getStoredUserRole();
    const backRoute = isInterviewer() ? ROUTES.INTERVIEW_ASSIGNED : ROUTES.INTERVIEWS;

    useEffect(() => {
        const controller = new AbortController();
        loadInterviewDetails(id, controller.signal)
            .then((data) => setInterview(data))
            .catch((err) => {
                if (err?.name !== 'CanceledError') {
                    setError(getInterviewManagementErrorMessage(err, 'Failed to load interview details.'));
                }
            })
            .finally(() => {
                if (!controller.signal.aborted) setLoading(false);
            });
        return () => controller.abort();
    }, [id]);

    if (loading) return <div className="um-state">Loading interview details...</div>;

    if (error || !interview) {
        return (
            <div className="um-state">
                <div className="error-banner">{error || 'Interview not found.'}</div>
                <button type="button" className="btn-secondary" onClick={() => navigate(backRoute)}>
                    {role === USER_ROLES.INTERVIEWER ? 'Back to Assigned Interviews' : 'Back to Interviews'}
                </button>
            </div>
        );
    }

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Interview Details</h1>
                    <p>View-only interview record.</p>
                </div>
                <div className="table-actions">
                    <Link to={backRoute} className="btn-secondary">
                        {role === USER_ROLES.INTERVIEWER ? 'Back to Assigned Interviews' : 'Back to Interviews'}
                    </Link>
                    {interview.candidate_id ? <Link to={`/candidates/${interview.candidate_id}/resume`} state={{ returnTo: ROUTES.INTERVIEW_DETAILS.replace(':id', id) }} className="btn-secondary">View Resume</Link> : null}
                    {role === USER_ROLES.HR && interview.status !== 'INTERVIEW_COMPLETED' ? <Link to={ROUTES.INTERVIEW_EDIT.replace(':id', id)} className="btn-secondary">Edit Interview</Link> : null}
                    <Link to={ROUTES.INTERVIEW_FEEDBACK.replace(':id', id)} className="btn-secondary">View Feedback</Link>
                </div>
            </div>
            <div className="jm-details-layout">
                <section className="form-card">
                    <div className="jm-detail-grid">
                        <div className="jm-detail-item"><span className="jm-detail-label">Candidate</span><span className="jm-detail-value">{interview.candidate_name}</span></div>
                        <div className="jm-detail-item"><span className="jm-detail-label">Job</span><span className="jm-detail-value">{interview.job_title}</span></div>
                        <div className="jm-detail-item"><span className="jm-detail-label">Interviewer</span><span className="jm-detail-value">{interview.interviewer_name}</span></div>
                        <div className="jm-detail-item"><span className="jm-detail-label">Date</span><span className="jm-detail-value">{formatInterviewDate(interview.interview_date)}</span></div>
                        <div className="jm-detail-item"><span className="jm-detail-label">Time</span><span className="jm-detail-value">{interview.interview_time}</span></div>
                        <div className="jm-detail-item"><span className="jm-detail-label">Interview Status</span><span className="jm-detail-value">{interview.status || 'Not available'}</span></div>
                    </div>
                    <div className="form-section-header">
                        <h2 className="form-section-title">Focus Tech Areas</h2>
                    </div>
                    <div className="jm-skill-list jm-skill-list-spacious">
                        {(interview.focus_tech_areas || []).map((area) => <span key={area} className="jm-skill-pill">{area}</span>)}
                    </div>
                </section>
            </div>
        </div>
    );
};

export default InterviewDetailsScreen;
