import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import '../styles/candidate-management.css';
import { formatCandidateDateDisplay, getCandidateManagementErrorMessage } from '../utils/candidateManagement';
import { loadCandidateStatusHistory } from '../utils/pageLoaders';

/**
 * Render the candidate status history table.
 */
const CandidateStatusHistoryScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [candidate, setCandidate] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const controller = new AbortController();
        loadCandidateStatusHistory(id, controller.signal)
            .then(([candidateData, historyData]) => {
                setCandidate(candidateData);
                setHistory(Array.isArray(historyData) ? historyData : []);
            })
            .catch((err) => {
                if (err?.name !== 'CanceledError') setError(getCandidateManagementErrorMessage(err, 'Failed to load status history.'));
            })
            .finally(() => {
                if (!controller.signal.aborted) setLoading(false);
            });
        return () => controller.abort();
    }, [id]);

    if (loading) return <div className="um-state">Loading status history...</div>;

    if (error || !candidate) {
        return (
            <div className="um-state">
                <div className="error-banner">{error || 'Status history not found.'}</div>
                <button type="button" className="btn-secondary" onClick={() => navigate(`/candidates/${id}`)}>Back</button>
            </div>
        );
    }

    const defaultEntry = {
        previous_status: '—',
        new_status: 'PROFILE_CREATED',
        timestamp: candidate.created_at || candidate.createdAt,
    };
    const rows = [
        defaultEntry,
        ...history.filter((row) => !(row.new_status === 'PROFILE_CREATED' && row.timestamp === defaultEntry.timestamp)),
    ];

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Status History</h1>
                    <p>Candidate status change audit trail.</p>
                </div>
                <Link to={`/candidates/${id}`} className="btn-secondary">Back to Candidate</Link>
            </div>
            <div className="table-card">
                <table className="um-table">
                    <thead>
                        <tr>
                            <th>Previous Status</th>
                            <th>New Status</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows.map((row, index) => (
                            <tr key={`${row.timestamp || index}-${index}`}>
                                <td data-label="Previous Status">{row.previous_status || '—'}</td>
                                <td data-label="New Status">{row.new_status || '—'}</td>
                                <td data-label="Date">{formatCandidateDateDisplay(row.timestamp)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default CandidateStatusHistoryScreen;
