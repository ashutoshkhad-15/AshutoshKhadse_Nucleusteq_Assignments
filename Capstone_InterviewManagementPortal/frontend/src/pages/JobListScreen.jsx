import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import useDebouncedValue from '../hooks/useDebouncedValue';
import JobCard from '../components/jobs/JobCard';
import { jobService } from '../services/jobService';
import '../styles/job-management.css';
import { getJobManagementErrorMessage, JOB_LIST_SKELETON_COUNT, JOB_SEARCH_DEBOUNCE_MS, throttle } from '../utils/jobManagement';

const HR_ROLE = 'HR';

/**
 * Renders the job list page.
 */
const JobListScreen = () => {
    const [jobs, setJobs] = useState([]);
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
    const role = localStorage.getItem('userRole');
    const canManageJobs = role === HR_ROLE;
    const debouncedSearchTerm = useDebouncedValue(searchTerm, JOB_SEARCH_DEBOUNCE_MS);
    const normalizedSearch = debouncedSearchTerm.trim();

    useEffect(() => {
        if (!location.state?.successMessage) return;
        setSuccessMessage(location.state.successMessage);
        navigate(location.pathname, { replace: true });
    }, [location.pathname, location.state, navigate]);

    useEffect(() => setCurrentPage(1), [normalizedSearch]);

    useEffect(() => {
        const controller = new AbortController();
        const loadJobs = async () => {
            try {
                setError(null);
                if (loading && jobs.length === 0) setLoading(true);
                else setSearching(true);
                const response = await jobService.getAllJobs(normalizedSearch, { signal: controller.signal, params: { page: currentPage, limit: itemsPerPage } });
                setJobs(Array.isArray(response?.data) ? response.data : []);
                setPagination(response?.meta || { page: 1, limit: 10, total_items: 0, total_pages: 1 });
            } catch (err) {
                if (err?.name !== 'CanceledError') setError(getJobManagementErrorMessage(err, 'Failed to load job descriptions.'));
            } finally {
                setLoading(false);
                setSearching(false);
            }
        };
        loadJobs();
        return () => controller.abort();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [normalizedSearch, currentPage, itemsPerPage]);

    useEffect(() => {
        const handleResize = throttle(() => {
            setItemsPerPage(window.innerWidth < 900 ? 6 : 10);
        }, 200);
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    if (loading) {
        return <div className="um-container"><div className="jm-skeleton-grid">{Array.from({ length: JOB_LIST_SKELETON_COUNT }).map((_, index) => <div key={index} className="jm-skeleton-card" />)}</div></div>;
    }

    if (error && jobs.length === 0) {
        return <div className="um-state"><div className="error-banner">{error}</div><button type="button" className="btn-secondary" onClick={() => window.location.reload()}>Retry</button></div>;
    }

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Hiring</p>
                    <h1>Job Descriptions</h1>
                    <p>Review openings, manage job details, and keep hiring requirements aligned across teams.</p>
                </div>
                {canManageJobs ? <button onClick={() => navigate('/jobs/create')} className="btn-primary">Create Job</button> : null}
            </div>

            <div className="table-card">
                {successMessage ? <div className="success-banner">{successMessage}</div> : null}
                {error ? <div className="error-banner">{error}</div> : null}
                <div className="um-toolbar">
                    <input id="job-search-input" type="text" placeholder="Search by title, role, skills, or location" value={searchTerm} onChange={(event) => setSearchTerm(event.target.value)} className="um-search-input" />
                </div>

                {searching ? <div className="empty-state">Searching jobs...</div> : jobs.length === 0 ? <div className="empty-state">{normalizedSearch ? 'No jobs matched your search.' : 'No jobs available yet.'}</div> : (
                    <div className="jm-job-card-grid">
                        {jobs.map((job) => <JobCard key={job._id} job={job} canManageJobs={canManageJobs} />)}
                    </div>
                )}

                {pagination.total_pages > 1 ? (
                    <div className="um-pagination">
                        <span className="pagination-info">Showing {jobs.length === 0 ? 0 : ((pagination.page || currentPage) - 1) * (pagination.limit || itemsPerPage) + 1} to {((pagination.page || currentPage) - 1) * (pagination.limit || itemsPerPage) + jobs.length} of {pagination.total_items} jobs</span>
                        <div className="pagination-buttons">
                            <button onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))} disabled={currentPage === 1} className="btn-page">Previous</button>
                            <button onClick={() => setCurrentPage((prev) => Math.min(prev + 1, pagination.total_pages || 1))} disabled={currentPage === (pagination.total_pages || 1)} className="btn-page">Next</button>
                        </div>
                    </div>
                ) : null}
            </div>
        </div>
    );
};

export default JobListScreen;
