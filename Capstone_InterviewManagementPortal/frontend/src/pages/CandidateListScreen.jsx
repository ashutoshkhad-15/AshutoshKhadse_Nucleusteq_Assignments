import { Eye, Pencil, Plus, Search, Users } from 'lucide-react';
import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import useDebouncedValue from '../hooks/useDebouncedValue';
import { candidateService } from '../services/candidateService';
import '../styles/candidate-management.css';
import { formatCandidateDate, getCandidateAppliedJobLabel, getCandidateManagementErrorMessage } from '../utils/candidateManagement';

const HR_ROLE = 'HR';

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
    const role = localStorage.getItem('userRole');
    const canManageCandidates = role === HR_ROLE;
    const debouncedSearchTerm = useDebouncedValue(searchInput, 500);
    const normalizedSearchTerm = debouncedSearchTerm.trim();
    const requestParams = useMemo(() => ({ search: normalizedSearchTerm }), [normalizedSearchTerm]);

    useEffect(() => {
        if (!location.state?.successMessage) return;
        setSuccessMessage(location.state.successMessage);
        navigate(location.pathname, { replace: true });
    }, [location.pathname, location.state, navigate]);

    useEffect(() => setCurrentPage(1), [normalizedSearchTerm]);

    useEffect(() => {
        const controller = new AbortController();
        const timeoutId = window.setTimeout(async () => {
            try {
                if (!didInitRef.current) {
                    didInitRef.current = true;
                    setLoading(true);
                } else {
                    setSearching(true);
                }
                const response = await candidateService.getAllCandidates(requestParams.search, { signal: controller.signal, params: { page: currentPage, limit: itemsPerPage } });
                setCandidates(Array.isArray(response?.data) ? response.data : []);
                setPagination(response?.meta || { page: 1, limit: 10, total_items: 0, total_pages: 1 });
                setError(null);
            } catch (err) {
                if (err?.name !== 'CanceledError') setError(getCandidateManagementErrorMessage(err, 'Failed to load candidates.'));
            } finally {
                if (!controller.signal.aborted) {
                    setLoading(false);
                    setSearching(false);
                }
            }
        }, 20);
        return () => {
            window.clearTimeout(timeoutId);
            controller.abort();
        };
    }, [requestParams, currentPage, itemsPerPage]);

    const totalPages = pagination.total_pages || 1;
    const startIndex = ((pagination.page || currentPage) - 1) * (pagination.limit || itemsPerPage);

    if (loading) return <div className="um-state">Loading candidates...</div>;

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Candidate Management</h1>
                    <p>Search candidates by name, email, mobile, company, or applied job.</p>
                </div>
                {canManageCandidates ? <button type="button" onClick={() => navigate('/candidates/create')} className="btn-primary btn-icon"><Plus size={18} className="icon-inline" /> Register Candidate</button> : null}
            </div>
            <div className="table-card">
                {successMessage ? <div className="success-banner">{successMessage}</div> : null}
                {error ? <div className="error-banner">{error}</div> : null}
                <div className="um-toolbar">
                    <label className="visually-hidden" htmlFor="candidate-search-input">Search candidates</label>
                    <div className="search-input-wrapper">
                        <Search size={18} className="icon-inline" />
                        <input id="candidate-search-input" type="text" placeholder="Search by name, email, mobile, company, or job" value={searchInput} onChange={(e) => setSearchInput(e.target.value)} className="um-search-input" />
                    </div>
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
                                    <th>Registration Date</th>
                                    <th className="align-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {candidates.map((candidate) => (
                                    <tr key={candidate._id}>
                                        <td data-label="Candidate" className="um-user-email"><div className="user-email-cell"><Users size={16} className="icon-inline" /> {candidate.first_name} {candidate.last_name}</div></td>
                                        <td data-label="Email">{candidate.email}</td>
                                        <td data-label="Mobile">{candidate.mobile}</td>
                                        <td data-label="Current Company">{candidate.current_company || 'Not specified'}</td>
                                        <td data-label="Applied Job">{getCandidateAppliedJobLabel(candidate)}</td>
                                        <td data-label="Experience">{candidate.total_experience}</td>
                                        <td data-label="Registration Date">{formatCandidateDate(candidate.created_at || candidate.createdAt)}</td>
                                        <td data-label="Actions" className="align-right">
                                            <div className="table-actions">
                                                <Link to={`/candidates/${candidate._id}`} className="action-edit"><Eye size={14} className="icon-inline" /> View</Link>
                                                {canManageCandidates ? <Link to={`/candidates/edit/${candidate._id}`} className="action-edit"><Pencil size={14} className="icon-inline" /> Edit</Link> : null}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {totalPages > 1 ? (
                            <div className="um-pagination">
                                <span className="pagination-info">Showing {candidates.length === 0 ? 0 : startIndex + 1} to {startIndex + candidates.length} of {pagination.total_items} candidates</span>
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
