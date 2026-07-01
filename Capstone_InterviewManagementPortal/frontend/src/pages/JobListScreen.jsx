import { Eye, Plus, RefreshCw, Search, SquarePen } from 'lucide-react';
import { useCallback, useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import JobPageHeader from '../components/jobs/JobPageHeader';
import JobStatusBadge from '../components/jobs/JobStatusBadge';
import { jobService } from '../services/jobService';
import '../styles/job-management.css';
import {
    getJobItemsPerPage,
    getJobManagementErrorMessage,
    JOB_LIST_SKELETON_COUNT,
    JOB_SEARCH_DEBOUNCE_MS,
    JOB_STATUS_OPTIONS,
    throttle,
    useDebouncedValue,
} from '../utils/jobManagement';

const HR_ROLE = 'HR';

/**
 * Display the searchable job listing and role-aware management actions.
 *
 * @returns {JSX.Element} Job listing screen.
 */
const JobListScreen = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [initialLoad, setInitialLoad] = useState(true);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');
    const [searchInput, setSearchInput] = useState('');
    const [statusFilter, setStatusFilter] = useState('ALL');
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(() => getJobItemsPerPage(window.innerWidth));
    const [statusUpdateId, setStatusUpdateId] = useState('');

    const navigate = useNavigate();
    const location = useLocation();
    const role = localStorage.getItem('userRole');
    const canManageJobs = role === HR_ROLE;
    const debouncedSearchTerm = useDebouncedValue(searchInput, JOB_SEARCH_DEBOUNCE_MS);

    /**
     * Load the visible job list using the current search and filter state.
     *
     * @returns {Promise<void>}
     */
    const loadJobs = useCallback(async () => {
    try {
        if (initialLoad) {
            setLoading(true);
        } 

        const params = {};

        if (debouncedSearchTerm.trim()) {
            params.search = debouncedSearchTerm.trim();
        }

        if (statusFilter !== 'ALL') {
            params.status_filter = statusFilter;
        }

        const data = await jobService.getAllJobs(params);

        setJobs(Array.isArray(data) ? data : []);
        setError(null);
    } catch (err) {
        setError(
            getJobManagementErrorMessage(
                err,
                'Failed to load job descriptions.'
            )
        );
    } finally {
        setLoading(false);
        setInitialLoad(false);
    }
}, [debouncedSearchTerm, statusFilter, initialLoad]);

    useEffect(() => {
        if (!location.state?.successMessage) return;
        setSuccessMessage(location.state.successMessage);
        navigate(location.pathname, { replace: true });
    }, [location.pathname, location.state, navigate]);

    useEffect(() => {
        loadJobs();
    }, [loadJobs]);

    useEffect(() => {
        // Reset pagination whenever the active search or filter changes.
        setCurrentPage(1);
    }, [debouncedSearchTerm, statusFilter]);

    useEffect(() => {
        const handleResize = throttle(() => {
            setItemsPerPage(getJobItemsPerPage(window.innerWidth));
        }, 200);

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    /**
     * Open or close a job posting after confirmation.
     *
     * @param {object} job - Selected job.
     * @returns {Promise<void>}
     */
    const handleToggleStatus = async (job) => {
        const nextStatus = !job.is_active;
        const actionLabel = nextStatus ? 'reopen' : 'close';
        const confirmationMessage = nextStatus
            ? `Are you sure you want to reopen ${job.title}?`
            : `Are you sure you want to close ${job.title}?`;

        if (!window.confirm(confirmationMessage)) return;

        try {
            setStatusUpdateId(job._id);
            await jobService.updateJob(job._id, { is_active: nextStatus });
            await loadJobs();
            setSuccessMessage(`Job "${job.title}" ${actionLabel}ed successfully.`);
            setError(null);
        } catch (err) {
            setError(getJobManagementErrorMessage(err, `Failed to ${actionLabel} job.`));
        } finally {
            setStatusUpdateId('');
        }
    };

    const totalPages = Math.max(1, Math.ceil(jobs.length / itemsPerPage));
    const startIndex = (currentPage - 1) * itemsPerPage;
    const currentJobs = jobs.slice(startIndex, startIndex + itemsPerPage);

    if (loading) {
        return (
            <div className="um-container">
                <div className="jm-skeleton-grid" aria-hidden="true">
                    {Array.from({ length: JOB_LIST_SKELETON_COUNT }).map((_, index) => (
                        <div key={index} className="jm-skeleton-card" />
                    ))}
                </div>
            </div>
        );
    }

    if (error && jobs.length === 0) {
        return (
            <div className="um-state">
                <div className="error-banner">{error}</div>
                <button type="button" className="btn-secondary jm-button-with-icon" onClick={loadJobs}>
                    <RefreshCw size={16} aria-hidden="true" />
                    Retry
                </button>
            </div>
        );
    }

    return (
        <div className="um-container">
            <JobPageHeader
                eyebrow="Hiring"
                title="Job Descriptions"
                description="Review active openings, manage job details, and keep hiring requirements aligned across teams."
                actions={canManageJobs ? (
                    <button onClick={() => navigate('/jobs/create')} className="btn-primary jm-button-with-icon">
                        <Plus size={16} aria-hidden="true" />
                        Create Job
                    </button>
                ) : null}
            />

            <div className="table-card">
                {successMessage ? <div className="success-banner">{successMessage}</div> : null}
                {error ? <div className="error-banner jm-inline-banner">{error}</div> : null}

                <div className="um-toolbar jm-toolbar">
                    <div className="jm-search-field">
                        <Search size={18} aria-hidden="true" className="jm-search-icon" />
                        <input
                            type="text"
                            placeholder="Search by title, department, skill, or location..."
                            value={searchInput}
                            onChange={(event) => setSearchInput(event.target.value)}
                            className="um-search-input jm-search-input"
                        />
                    </div>
                    <select
                        value={statusFilter}
                        onChange={(event) => setStatusFilter(event.target.value)}
                        className="um-filter-select"
                    >
                        {JOB_STATUS_OPTIONS.map((option) => (
                            <option key={option.value} value={option.value}>
                                {option.label}
                            </option>
                        ))}
                    </select>
                </div>

                {jobs.length === 0 ? (
                    <div className="empty-state jm-empty-state">
                        <h2>No jobs found</h2>
                        <p>Try broadening the search or changing the status filter.</p>
                    </div>
                ) : (
                    <div className="jm-job-grid">
                        {currentJobs.map((job) => (
                            <article key={job._id} className="jm-job-card">
                                <div className="jm-job-card-top">
                                    <div>
                                        <div className="jm-job-heading">
                                            <h2>{job.title}</h2>
                                            <JobStatusBadge isActive={job.is_active} />
                                        </div>
                                        <p className="jm-job-meta">{job.department} | {job.location}</p>
                                    </div>
                                    <span className="badge-role">{job.experience_required}</span>
                                </div>

                                <p className="jm-job-description">{job.description}</p>

                                <div className="jm-skill-list">
                                    {(job.skills || []).slice(0, 4).map((skill) => (
                                        <span key={skill} className="jm-skill-pill">{skill}</span>
                                    ))}
                                    {(job.skills || []).length > 4 ? (
                                        <span className="jm-skill-pill jm-skill-pill-muted">+{job.skills.length - 4} more</span>
                                    ) : null}
                                </div>

                                <div className="table-actions jm-job-actions">
                                    <Link to={`/jobs/${job._id}`} className="action-edit">
                                        <Eye size={16} aria-hidden="true" />
                                        View Details
                                    </Link>
                                    {canManageJobs ? (
                                        <>
                                            <Link to={`/jobs/edit/${job._id}`} className="action-edit">
                                                <SquarePen size={16} aria-hidden="true" />
                                                Edit
                                            </Link>
                                            <button
                                                onClick={() => handleToggleStatus(job)}
                                                disabled={statusUpdateId === job._id}
                                                className={job.is_active ? 'action-disable' : 'action-enable'}
                                            >
                                                {statusUpdateId === job._id ? 'Updating...' : job.is_active ? 'Close' : 'Reopen'}
                                            </button>
                                        </>
                                    ) : null}
                                </div>
                            </article>
                        ))}
                    </div>
                )}

                {jobs.length > 0 && totalPages > 1 ? (
                    <div className="um-pagination">
                        <span className="pagination-info">
                            Showing {startIndex + 1} to {Math.min(startIndex + itemsPerPage, jobs.length)} of {jobs.length} jobs
                        </span>
                        <div className="pagination-buttons">
                            <button
                                onClick={() => setCurrentPage((page) => Math.max(page - 1, 1))}
                                disabled={currentPage === 1}
                                className="btn-page"
                            >
                                Previous
                            </button>
                            <button
                                onClick={() => setCurrentPage((page) => Math.min(page + 1, totalPages))}
                                disabled={currentPage === totalPages}
                                className="btn-page"
                            >
                                Next
                            </button>
                        </div>
                    </div>
                ) : null}
            </div>
        </div>
    );
};

export default JobListScreen;
