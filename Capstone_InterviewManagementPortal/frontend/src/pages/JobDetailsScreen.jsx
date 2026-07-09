import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import JobPageHeader from '../components/jobs/JobPageHeader';
import { USER_ROLES } from '../constants/roles';
import { getJobManagementErrorMessage } from '../utils/jobManagement';
import { loadJobDetails } from '../utils/pageLoaders';
import '../styles/job-management.css';

/**
 * Display a single job description with role-aware actions.
 *
 * @returns {JSX.Element} Job details screen.
 */
const JobDetailsScreen = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [job, setJob] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const role = localStorage.getItem('userRole');
    const canManageJobs = role === USER_ROLES.HR;

    useEffect(() => {
        /**
         * Fetch the selected job details.
         *
         * @returns {Promise<void>}
         */
        const controller = new AbortController();
        const timeoutId = window.setTimeout(() => {
            try {
                setLoading(true);
                loadJobDetails(id, controller.signal)
                    .then((data) => {
                        setJob(data);
                        setError(null);
                    })
                    .catch((err) => {
                        if (err?.name === 'CanceledError') {
                            return;
                        }
                        setError(getJobManagementErrorMessage(err, 'Failed to load job details.'));
                    })
                    .finally(() => {
                        if (!controller.signal.aborted) {
                            setLoading(false);
                        }
                    });
            } catch (err) {
                if (err?.name !== 'CanceledError') {
                    setError(getJobManagementErrorMessage(err, 'Failed to load job details.'));
                }
            }
        }, 20);

        return () => {
            window.clearTimeout(timeoutId);
            controller.abort();
        };
    }, [id]);

    if (loading) {
        return <div className="um-state">Loading job details...</div>;
    }

    if (error || !job) {
        return (
            <div className="um-state">
                <div className="error-banner">{error || 'Job description not found.'}</div>
                <div className="form-actions jm-centered-actions">
                    <button type="button" className="btn-secondary" onClick={() => navigate('/jobs')}>Back to Jobs</button>
                </div>
            </div>
        );
    }

    return (
        <div className="um-container">
            <JobPageHeader
                eyebrow="Hiring"
                title={job.jobTitle || job.title}
                description={`${job.jobRole || job.department} | ${job.location}`}
                actions={(
                    <>
                        <button type="button" onClick={() => navigate('/jobs')} className="btn-secondary">Back to Jobs</button>
                        {canManageJobs ? (
                            <Link to={`/jobs/edit/${job._id}`} className="btn-primary">Edit Job</Link>
                        ) : null}
                    </>
                )}
            />

            <div className="jm-details-layout">
                <section className="form-card">
                    <div className="form-section-header">
                        <h2 className="form-section-title">Role Overview</h2>
                        <p className="form-section-copy">Core context for recruiters and interview panel members.</p>
                    </div>

                    <div className="jm-detail-grid">
                        <div className="jm-detail-item">
                            <span className="jm-detail-label">Experience</span>
                            <span className="jm-detail-value">{job.experienceRequired ?? job.experience_required}</span>
                        </div>
                        <div className="jm-detail-item">
                            <span className="jm-detail-label">Job Role</span>
                            <span className="jm-detail-value">{job.jobRole || job.department}</span>
                        </div>
                        <div className="jm-detail-item">
                            <span className="jm-detail-label">Location</span>
                            <span className="jm-detail-value">{job.location}</span>
                        </div>
                    </div>
                </section>

                <section className="form-card">
                    <div className="form-section-header">
                        <h2 className="form-section-title">Required Skills</h2>
                        <p className="form-section-copy">Skills currently expected for candidate evaluation.</p>
                    </div>

                    <div className="jm-skill-list jm-skill-list-spacious">
                        {(job.requiredSkills || job.skills || []).map((skill) => (
                            <span key={skill} className="jm-skill-pill">{skill}</span>
                        ))}
                    </div>
                </section>

                <section className="form-card">
                    <div className="form-section-header">
                        <h2 className="form-section-title">Job Description</h2>
                        <p className="form-section-copy">Detailed responsibilities and role expectations.</p>
                    </div>

                    <div className="jm-rich-copy">
                        {job.jobDetails || job.description}
                    </div>
                </section>
            </div>
        </div>
    );
};

export default JobDetailsScreen;
