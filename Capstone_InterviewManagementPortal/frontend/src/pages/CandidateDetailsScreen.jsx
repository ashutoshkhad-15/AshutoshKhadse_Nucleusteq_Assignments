import { ArrowLeft, Mail, Phone, SquarePen, Users } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { candidateService } from '../services/candidateService';
import '../styles/candidate-management.css';
import { formatCandidateDate, getCandidateAppliedJobLabel, getCandidateManagementErrorMessage } from '../utils/candidateManagement';

const HR_ROLE = 'HR';

const CandidateDetailsScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [candidate, setCandidate] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const role = localStorage.getItem('userRole');
    const canManageCandidates = role === HR_ROLE;

    useEffect(() => {
        const controller = new AbortController();
        (async () => {
            try {
                const data = await candidateService.getCandidateById(id, { signal: controller.signal });
                setCandidate(data);
            } catch (err) {
                if (err?.name !== 'CanceledError') setError(getCandidateManagementErrorMessage(err, 'Failed to load candidate details.'));
            } finally {
                if (!controller.signal.aborted) setLoading(false);
            }
        })();
        return () => controller.abort();
    }, [id]);

    if (loading) return <div className="um-state">Loading candidate details...</div>;

    if (error || !candidate) {
        return (
            <div className="um-state">
                <div className="error-banner">{error || 'Candidate profile not found.'}</div>
                <div className="form-actions jm-centered-actions">
                    <button type="button" className="btn-secondary jm-button-with-icon" onClick={() => navigate('/candidates')}>
                        <ArrowLeft size={16} aria-hidden="true" /> Back to Candidates
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>{candidate.first_name} {candidate.last_name}</h1>
                    <p>Candidate profile and applied job details.</p>
                </div>
                <div className="table-actions jm-header-actions">
                    <button type="button" onClick={() => navigate('/candidates')} className="btn-secondary jm-button-with-icon">
                        <ArrowLeft size={16} aria-hidden="true" /> Back to Candidates
                    </button>
                    {canManageCandidates ? (
                        <Link to={`/candidates/edit/${candidate._id}`} className="btn-primary jm-link-button jm-button-with-icon">
                            <SquarePen size={16} aria-hidden="true" /> Edit Candidate
                        </Link>
                    ) : null}
                </div>
            </div>
            <div className="jm-details-layout">
                <section className="form-card">
                    <div className="form-section-header">
                        <h2 className="form-section-title">Profile Overview</h2>
                    </div>
                    <div className="jm-detail-grid">
                        <div className="jm-detail-item"><span className="jm-detail-label">Email</span><span className="jm-detail-value"><Mail size={16} />{candidate.email}</span></div>
                        <div className="jm-detail-item"><span className="jm-detail-label">Mobile</span><span className="jm-detail-value"><Phone size={16} />{candidate.mobile}</span></div>
                        <div className="jm-detail-item"><span className="jm-detail-label">Current Company</span><span className="jm-detail-value"><Users size={16} />{candidate.current_company || 'Not specified'}</span></div>
                        <div className="jm-detail-item"><span className="jm-detail-label">Total Experience</span><span className="jm-detail-value">{candidate.total_experience}</span></div>
                        <div className="jm-detail-item"><span className="jm-detail-label">Applied Job</span><span className="jm-detail-value">{getCandidateAppliedJobLabel(candidate)}</span></div>
                        <div className="jm-detail-item"><span className="jm-detail-label">Registration Date</span><span className="jm-detail-value">{formatCandidateDate(candidate.created_at || candidate.createdAt)}</span></div>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default CandidateDetailsScreen;
