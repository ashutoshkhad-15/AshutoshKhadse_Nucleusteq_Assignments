import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import useDebouncedValue from '../hooks/useDebouncedValue';
import '../styles/interview-management.css';
import { formatInterviewDate, getInterviewManagementErrorMessage, throttle } from '../utils/interviewManagement';
import { USER_ROLES } from '../constants/roles';
import { ROUTES } from '../constants/routes';
import { loadInterviewList } from '../utils/pageLoaders';
import { getListPagination, getListRows, isCanceledRequest, getPaginationRange } from '../utils/listPage';
import { getStoredUserRole } from '../utils/session';

/**
 * Render the interview list with server-side search and pagination.
 */
const InterviewListScreen = () => {
    const [interviews, setInterviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searching, setSearching] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [pagination, setPagination] = useState({ page: 1, limit: 10, total_items: 0, total_pages: 1 });
    const navigate = useNavigate();
    const location = useLocation();
    const didInitRef = useRef(false);
    const throttledLoadRef = useRef(null);
    const role = getStoredUserRole();
    const debouncedSearchTerm = useDebouncedValue(searchTerm, 500);
    const normalizedSearch = debouncedSearchTerm.trim();
    const requestSearch = useMemo(() => normalizedSearch, [normalizedSearch]);

    useEffect(() => {
        if (!location.state?.successMessage) return;
        setSuccessMessage(location.state.successMessage);
        navigate(location.pathname, { replace: true });
    }, [location.pathname, location.state, navigate]);

    useEffect(() => setCurrentPage(1), [requestSearch]);

    useEffect(() => {
        if (!throttledLoadRef.current) {
            throttledLoadRef.current = throttle((requestParams, controller) => {
                if (!didInitRef.current) {
                    didInitRef.current = true;
                    setLoading(true);
                } else {
                    setSearching(true);
                }
                loadInterviewList(requestParams.search, requestParams.page, requestParams.limit, controller.signal)
                    .then((response) => {
                        setInterviews(getListRows(response));
                        setPagination(getListPagination(response));
                        setError(null);
                    })
                    .catch((err) => {
                        if (!isCanceledRequest(err)) {
                            setError(getInterviewManagementErrorMessage(err, 'Failed to load interviews.'));
                        }
                    })
                    .finally(() => {
                        if (!controller.signal.aborted) {
                            setLoading(false);
                            setSearching(false);
                        }
                    });
            }, 250);
        }

        const controller = new AbortController();
        throttledLoadRef.current({ search: requestSearch, page: currentPage, limit: itemsPerPage }, controller);
        return () => {
            controller.abort();
        };
    }, [requestSearch, currentPage, itemsPerPage]);

    useEffect(() => {
        const handleResize = throttle(() => {
            setItemsPerPage(window.innerWidth < 900 ? 6 : 10);
        }, 200);
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    if (loading) {
        return <div className="um-state">Loading interviews...</div>;
    }

    const [startIndex, endIndex] = getPaginationRange(pagination, currentPage, itemsPerPage, interviews.length);

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Interview Scheduling</h1>
                    <p>Search interviews by candidate, job title, interviewer, or focus tech area.</p>
                </div>
                {role === USER_ROLES.HR ? <button type="button" onClick={() => navigate(ROUTES.INTERVIEW_SCHEDULE)} className="btn-primary">Schedule Interview</button> : null}
            </div>

            <div className="table-card">
                {successMessage ? <div className="success-banner">{successMessage}</div> : null}
                {error ? <div className="error-banner">{error}</div> : null}
                <div className="um-toolbar">
                    <input id="interview-search-input" type="text" placeholder="Search by candidate, job, interviewer, or tech area" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="um-search-input" />
                </div>
                {searching ? <div className="empty-state">Searching interviews...</div> : interviews.length === 0 ? <div className="empty-state">{normalizedSearch ? 'No interviews matched your search.' : 'No interviews scheduled yet.'}</div> : (
                    <>
                        <table className="um-table">
                            <thead>
                                <tr>
                                    <th>Candidate</th>
                                    <th>Job Title</th>
                                    <th>Interviewer</th>
                                    <th>Date</th>
                                    <th>Time</th>
                                    <th>Focus Tech Areas</th>
                                    <th className="align-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {interviews.map((interview) => (
                                    <tr key={interview._id}>
                                        <td data-label="Candidate">{interview.candidate_name}</td>
                                        <td data-label="Job Title">{interview.job_title}</td>
                                        <td data-label="Interviewer">{interview.interviewer_name}</td>
                                        <td data-label="Date">{formatInterviewDate(interview.interview_date)}</td>
                                        <td data-label="Time">{interview.interview_time}</td>
                                        <td data-label="Focus Tech Areas">{Array.isArray(interview.focus_tech_areas) ? interview.focus_tech_areas.join(', ') : 'Not available'}</td>
                                        <td data-label="Actions" className="align-right">
                                            <div className="table-actions">
                                                <Link to={ROUTES.INTERVIEW_DETAILS.replace(':id', interview._id)} className="btn-secondary">View</Link>
                                                {role === USER_ROLES.HR ? <Link to={ROUTES.INTERVIEW_EDIT.replace(':id', interview._id)} className="btn-secondary">Edit</Link> : null}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {pagination.total_pages > 1 ? (
                            <div className="um-pagination">
                                <span className="pagination-info">Showing {startIndex} to {endIndex} of {pagination.total_items} interviews</span>
                                <div className="pagination-buttons">
                                    <button type="button" onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))} disabled={currentPage === 1} className="btn-page">Previous</button>
                                    <button type="button" onClick={() => setCurrentPage((prev) => Math.min(prev + 1, pagination.total_pages || 1))} disabled={currentPage === (pagination.total_pages || 1)} className="btn-page">Next</button>
                                </div>
                            </div>
                        ) : null}
                    </>
                )}
            </div>
        </div>
    );
};

export default InterviewListScreen;
