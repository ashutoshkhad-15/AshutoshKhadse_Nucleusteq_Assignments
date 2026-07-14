import { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import '../styles/interview-management.css';
import { formatInterviewDate, getInterviewManagementErrorMessage } from '../utils/interviewManagement';
import { loadAssignedInterviews } from '../utils/pageLoaders';

/**
 * Render the assigned interviews list for interviewers.
 */
const AssignedInterviewsScreen = () => {
    const [interviews, setInterviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        if (!location.state?.successMessage) return;
        setSuccessMessage(location.state.successMessage);
        navigate(location.pathname, { replace: true });
    }, [location.pathname, location.state, navigate]);

    useEffect(() => {
        const controller = new AbortController();
        loadAssignedInterviews(controller.signal)
            .then((response) => setInterviews(Array.isArray(response?.data) ? response.data : []))
            .catch((err) => {
                if (err?.name !== 'CanceledError') setError(getInterviewManagementErrorMessage(err, 'Failed to load assigned interviews.'));
            })
            .finally(() => {
                if (!controller.signal.aborted) setLoading(false);
            });
        return () => controller.abort();
    }, []);

    const visibleInterviews = interviews;

    if (loading) return <div className="um-state">Loading assigned interviews...</div>;

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Assigned Interviews</h1>
                    <p>Interviews assigned to the logged-in interviewer.</p>
                </div>
            </div>
            <div className="table-card">
                {successMessage ? <div className="success-banner">{successMessage}</div> : null}
                {error ? <div className="error-banner">{error}</div> : null}
                {visibleInterviews.length === 0 ? <div className="empty-state">No assigned interviews available.</div> : (
                    <table className="um-table">
                        <thead>
                            <tr>
                                <th>Candidate</th>
                                <th>Job Title</th>
                                <th>Date</th>
                                <th>Time</th>
                                <th className="align-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {visibleInterviews.map((interview) => (
                                <tr key={interview._id}>
                                    <td data-label="Candidate">{interview.candidate_name}</td>
                                    <td data-label="Job Title">{interview.job_title}</td>
                                    <td data-label="Date">{formatInterviewDate(interview.interview_date)}</td>
                                    <td data-label="Time">{interview.interview_time}</td>
                                    <td data-label="Actions" className="align-right">
                                        <div className="table-actions">
                                            <Link to={`/interviews/${interview._id}`} className="btn-primary">View Details</Link>
                                            <Link to={`/interviews/${interview._id}/feedback`} className="btn-secondary">Feedback</Link>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default AssignedInterviewsScreen;
