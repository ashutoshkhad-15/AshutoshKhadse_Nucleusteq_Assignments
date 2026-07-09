import { useEffect, useState } from 'react';
import useDebouncedValue from '../../hooks/useDebouncedValue';
import { candidateService } from '../../services/candidateService';
import { mapJobsToOptions } from '../../utils/candidateManagement';
import '../../styles/candidate-management.css';

/**
 * Lets the user search and select a job for a candidate.
 */
const AppliedJobSelect = ({ value, onChange, error, disabled = false, initialJob }) => {
    const [open, setOpen] = useState(false);
    const [search, setSearch] = useState('');
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedJob, setSelectedJob] = useState(initialJob || null);
    const debouncedSearch = useDebouncedValue(search, 350);

    useEffect(() => {
        if (initialJob) setSelectedJob(initialJob);
    }, [initialJob]);

    useEffect(() => {
        const controller = new AbortController();
        const loadJobs = async () => {
            try {
                setLoading(true);
                const response = await candidateService.searchJobs(debouncedSearch, { signal: controller.signal, params: { limit: 20, page: 1 } });
                setJobs(mapJobsToOptions(Array.isArray(response?.data) ? response.data : []));
            } catch (err) {
                if (err?.name !== 'CanceledError') setJobs([]);
            } finally {
                if (!controller.signal.aborted) setLoading(false);
            }
        };

        if (open) loadJobs();
        return () => controller.abort();
    }, [debouncedSearch, open]);

    return (
        <div className="candidate-select-shell">
            <button
                type="button"
                className={`candidate-select-trigger ${error ? 'candidate-select-trigger-error' : ''}`}
                onClick={() => !disabled && setOpen((current) => !current)}
                disabled={disabled}
            >
                {selectedJob?.label || 'Select a job'}
            </button>

            {open ? (
                <div className="candidate-select-menu">
                    <input
                        type="text"
                        value={search}
                        onChange={(event) => setSearch(event.target.value)}
                        placeholder="Search jobs"
                        className="candidate-select-search-input"
                    />
                    <div className="candidate-select-options">
                        {loading ? <div className="candidate-select-empty">Loading jobs...</div> : null}
                        {!loading && jobs.length === 0 ? <div className="candidate-select-empty">No jobs found.</div> : null}
                        {!loading && jobs.map((job) => (
                            <button
                                key={job.value}
                                type="button"
                                className={`candidate-select-option ${value === job.value ? 'is-selected' : ''}`}
                                onClick={() => {
                                    setSelectedJob(job);
                                    onChange(job.value, job);
                                    setOpen(false);
                                }}
                            >
                                {job.label}
                            </button>
                        ))}
                    </div>
                </div>
            ) : null}
            <input type="hidden" value={value} />
        </div>
    );
};

export default AppliedJobSelect;
