import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import '../styles/candidate-management.css';
import { getCandidateManagementErrorMessage, getResumePdfUrl } from '../utils/candidateManagement';
import { loadCandidateResume } from '../utils/pageLoaders';

/**
 * Renders the native browser PDF preview for a candidate resume.
 */
const CandidateResumePreviewScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [resume, setResume] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const controller = new AbortController();
        loadCandidateResume(id, controller.signal)
            .then((data) => setResume(data))
            .catch((err) => {
                if (err?.name !== 'CanceledError') setError(getCandidateManagementErrorMessage(err, 'Failed to load resume.'));
            })
            .finally(() => {
                if (!controller.signal.aborted) setLoading(false);
            });
        return () => controller.abort();
    }, [id]);

    if (loading) return <div className="um-state">Loading resume...</div>;
    if (error || !resume) {
        return <div className="um-state"><div className="error-banner">{error || 'Resume not found.'}</div><button type="button" className="btn-secondary" onClick={() => navigate(`/candidates/${id}`)}>Back</button></div>;
    }

    const pdfUrl = getResumePdfUrl(resume);

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Resume Preview</h1>
                    <p>{resume.original_filename}</p>
                </div>
                <Link to={`/candidates/${id}`} className="btn-secondary">Back to Candidate</Link>
            </div>
            <div className="form-card">
                <iframe title="Resume Preview" src={pdfUrl} style={{ width: '100%', minHeight: '80vh', border: 0 }} />
            </div>
        </div>
    );
};

export default CandidateResumePreviewScreen;
