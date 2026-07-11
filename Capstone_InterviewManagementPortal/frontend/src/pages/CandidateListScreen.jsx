import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import useDebouncedValue from '../hooks/useDebouncedValue';
import '../styles/candidate-management.css';
import { canEditCandidates, canViewCandidates, getCandidateAppliedJobLabel, getCandidateDisplayName, getCandidateManagementErrorMessage } from '../utils/candidateManagement';
import { loadCandidateList } from '../utils/pageLoaders';
import { getListPagination, getListRows, isCanceledRequest, getPaginationRange } from '../utils/listPage';

/**
 * Renders the candidate list page.
 */
const CandidateListScreen = () => {
    const [candidates, setCandidates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searching, setSearching] = useState(false);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');
    const [searchInput, setSearchInput] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage] = useState(10);
    const [pagination, setPagination] = useState({ page: 1, limit: 10, total_items: 0, total_pages: 1 });
    const didInitRef = useRef(false);
    const navigate = useNavigate();
    const location = useLocation();
    const canView = canViewCandidates();
    const canEdit = canEditCandidates();
    const debouncedSearchTerm = useDebouncedValue(searchInput, 500);
    const normalizedSearchTerm = debouncedSearchTerm.trim();
    const requestSearch = useMemo(() => normalizedSearchTerm, [normalizedSearchTerm]);

    useEffect(() => {
        if (!location.state?.successMessage) return;
        setSuccessMessage(location.state.successMessage);
        navigate(location.pathname, { replace: true });
    }, [location.pathname, location.state, navigate]);

    useEffect(() => setCurrentPage(1), [normalizedSearchTerm]);

    useEffect(() => {
        const controller = new AbortController();
        const timeoutId = window.setTimeout(() => {
            const isInitialLoad = !didInitRef.current;

            if (isInitialLoad) {
                didInitRef.current = true;
                setLoading(true);
            } else {
                setSearching(true);
            }

            loadCandidateList(requestSearch, currentPage, itemsPerPage, controller.signal)
                .then((response) => {
                    setCandidates(getListRows(response));
                    setPagination(getListPagination(response));
                    setError(null);
                })
                .catch((err) => {
                    if (!isCanceledRequest(err)) {
                        setError(getCandidateManagementErrorMessage(err, 'Failed to load candidates.'));
                    }
                })
                .finally(() => {
                    if (!controller.signal.aborted) {
                        setLoading(false);
                        setSearching(false);
                    }
                });
        }, 20);
        return () => {
            window.clearTimeout(timeoutId);
            controller.abort();
        };
    }, [requestSearch, currentPage, itemsPerPage]);

    const totalPages = pagination.total_pages || 1;
    const [startIndex, endIndex] = getPaginationRange(pagination, currentPage, itemsPerPage, candidates.length);

    if (loading) return <div className="um-state">Loading candidates...</div>;
    if (!canView) return <div className="um-state"><div className="error-banner">You do not have permission to view candidates.</div></div>;

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Candidate Management</h1>
                    <p>Search candidates by name, email, mobile, company, or applied job.</p>
                </div>
                {canEdit ? <button type="button" onClick={() => navigate('/candidates/create')} className="btn-primary">Register Candidate</button> : null}
            </div>
            <div className="table-card">
                {successMessage ? <div className="success-banner">{successMessage}</div> : null}
                {error ? <div className="error-banner">{error}</div> : null}
                <div className="um-toolbar">
                    <input id="candidate-search-input" type="text" placeholder="Search by name, email, mobile, company, or job" value={searchInput} onChange={(e) => setSearchInput(e.target.value)} className="um-search-input" />
                </div>
                {searching ? <div className="empty-state">Searching candidates...</div> : candidates.length === 0 ? <div className="empty-state">{normalizedSearchTerm ? 'No candidates match your search criteria.' : 'No candidates are available yet.'}</div> : (
                    <>
                        <table className="um-table">
                            <thead>
                                <tr>
                                    <th>Candidate</th>
                                    <th>Email</th>
                                    <th>Mobile</th>
                                    <th>Current Company</th>
                                    <th>Applied Job</th>
                                    <th>Experience</th>
                                    <th className="align-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {candidates.map((candidate) => (
                                    <tr key={candidate._id}>
                                        <td data-label="Candidate" className="candidate-list-name" title={getCandidateDisplayName(candidate)}>{getCandidateDisplayName(candidate)}</td>
                                        <td data-label="Email" className="candidate-nowrap" title={candidate.email}>{candidate.email}</td>
                                        <td data-label="Mobile" className="candidate-nowrap" title={candidate.mobile}>{candidate.mobile}</td>
                                        <td data-label="Current Company" title={candidate.current_company || 'Not specified'}>{candidate.current_company || 'Not specified'}</td>
                                        <td data-label="Applied Job" title={getCandidateAppliedJobLabel(candidate)}>{getCandidateAppliedJobLabel(candidate)}</td>
                                        <td data-label="Experience">{candidate.total_experience}</td>
                                        <td data-label="Actions" className="align-right">
                                            <div className="table-actions candidate-table-actions">
                                                <Link to={`/candidates/${candidate._id}`} className="btn-secondary">View</Link>
                                                {canEdit ? <Link to={`/candidates/edit/${candidate._id}`} className="btn-secondary">Edit</Link> : null}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {totalPages > 1 ? (
                            <div className="um-pagination">
                                <span className="pagination-info">Showing {startIndex} to {endIndex} of {pagination.total_items} candidates</span>
                                <div className="pagination-buttons">
                                    <button type="button" onClick={() => setCurrentPage((page) => Math.max(page - 1, 1))} disabled={currentPage === 1} className="btn-page">Previous</button>
                                    <button type="button" onClick={() => setCurrentPage((page) => Math.min(page + 1, totalPages))} disabled={currentPage === totalPages} className="btn-page">Next</button>
                                </div>
                            </div>
                        ) : null}
                    </>
                )}
            </div>
        </div>
    );
};

export default CandidateListScreen;
