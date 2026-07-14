import { useEffect, useState } from 'react';
import DashboardStatCard from '../components/dashboard/DashboardStatCard';
import '../styles/interview-management.css';
import { USER_ROLES } from '../constants/roles';
import { canViewDashboard, getInterviewManagementErrorMessage } from '../utils/interviewManagement';
import { loadDashboardStats } from '../utils/pageLoaders';
import { getStoredUserRole } from '../utils/session';

/**
 * Render the role-based dashboard view.
 */
const DashboardScreen = () => {
    const role = getStoredUserRole();
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!canViewDashboard()) {
            setError('You do not have permission to view the dashboard.');
            setLoading(false);
            return;
        }
        const controller = new AbortController();
        loadDashboardStats(role, controller.signal)
            .then((data) => {
                setStats(data);
            })
            .catch((err) => {
                if (err?.name !== 'CanceledError') setError(getInterviewManagementErrorMessage(err, 'Failed to load dashboard statistics.'));
            })
            .finally(() => {
                if (!controller.signal.aborted) setLoading(false);
            });
        return () => controller.abort();
    }, [role]);

    if (loading) return <div className="um-state">Loading dashboard...</div>;
    if (error || !stats) return <div className="um-state"><div className="error-banner">{error || 'Dashboard data not available.'}</div></div>;

    const cards = role === USER_ROLES.INTERVIEWER
        ? [
            { label: 'Assigned Interviews', value: stats.assigned_interviews },
            { label: 'Pending Feedback', value: stats.pending_feedback },
            { label: 'Completed Feedback', value: stats.completed_feedback },
        ]
        : [
            { label: 'Total Jobs', value: stats.total_jobs },
            { label: 'Total Candidates', value: stats.total_candidates },
            { label: 'Scheduled Interviews', value: stats.scheduled_interviews },
            { label: 'Selected Candidates', value: stats.selected_candidates },
            { label: 'Rejected Candidates', value: stats.rejected_candidates },
        ];

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Overview</p>
                    <h1>Dashboard</h1>
                    <p>{role === USER_ROLES.INTERVIEWER ? 'Track your assigned interviews and feedback progress.' : 'Track core hiring metrics across the portal.'}</p>
                </div>
            </div>
            <div className="dashboard-grid">
                {cards.map((card) => <DashboardStatCard key={card.label} label={card.label} value={card.value} />)}
            </div>
        </div>
    );
};

export default DashboardScreen;
