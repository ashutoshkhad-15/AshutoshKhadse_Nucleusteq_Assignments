import { ChevronDown, Search } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import useDebouncedValue from '../../hooks/useDebouncedValue';
import { candidateService } from '../../services/candidateService';
import { mapJobsToOptions } from '../../utils/candidateManagement';
import '../../styles/candidate-management.css';

const AppliedJobSelect = ({
    value,
    onChange,
    error,
    disabled = false,
    initialJob,
}) => {
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
        const run = async () => {
            try {
                setLoading(true);
                const response = await candidateService.searchJobs(debouncedSearch, { signal: controller.signal, params: { limit: 20, page: 1 } });
                setJobs(mapJobsToOptions(Array.isArray(response?.data) ? response.data : []));
            } catch (err) {
                if (err?.name !== 'CanceledError') {
                    setJobs([]);
                }
            } finally {
                if (!controller.signal.aborted) setLoading(false);
            }
        };

        if (open) run();
        return () => controller.abort();
    }, [debouncedSearch, open]);

    const displayedOptions = useMemo(() => jobs, [jobs]);

    return (
        <div className="candidate-select-shell">
            <button
                type="button"
                className={`candidate-select-trigger ${error ? 'candidate-select-trigger-error' : ''}`}
                onClick={() => !disabled && setOpen((current) => !current)}
                disabled={disabled}
            >
                <span className="candidate-select-trigger-copy">
                    <span className="candidate-select-trigger-title">{selectedJob?.label || 'Select a job'}</span>
                    <span className="candidate-select-trigger-subtitle">{selectedJob?.description || 'Search jobs from the backend'}</span>
                </span>
                <ChevronDown size={16} />
            </button>

            {open ? (
                <div className="candidate-select-menu">
                    <div className="candidate-select-search">
                        <Search size={16} />
                        <input
                            type="text"
                            value={search}
                            onChange={(event) => setSearch(event.target.value)}
                            placeholder="Search job titles"
                            className="candidate-select-search-input"
                        />
                    </div>
                    <div className="candidate-select-options">
                        {loading ? <div className="candidate-select-empty">Loading jobs...</div> : null}
                        {!loading && displayedOptions.length === 0 ? <div className="candidate-select-empty">No jobs found.</div> : null}
                        {!loading && displayedOptions.map((job) => (
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
                                <span className="candidate-select-option-title">{job.label}</span>
                                <span className="candidate-select-option-copy">{job.description || 'Available job'}</span>
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
