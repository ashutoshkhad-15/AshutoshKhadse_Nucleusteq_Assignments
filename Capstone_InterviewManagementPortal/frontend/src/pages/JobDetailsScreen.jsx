import { ArrowLeft, BriefcaseBusiness, Building2, MapPin, SquarePen } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import JobPageHeader from '../components/jobs/JobPageHeader';
import JobStatusBadge from '../components/jobs/JobStatusBadge';
import { jobService } from '../services/jobService';
import { getJobManagementErrorMessage } from '../utils/jobManagement';
import '../styles/job-management.css';

const HR_ROLE = 'HR';

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
    const canManageJobs = role === HR_ROLE;

    useEffect(() => {
        /**
         * Fetch the selected job details.
         *
         * @returns {Promise<void>}
         */
        const fetchJob = async () => {
            try {
                setLoading(true);
                const data = await jobService.getJobById(id);
                setJob(data);
                setError(null);
            } catch (err) {
                setError(getJobManagementErrorMessage(err, 'Failed to load job details.'));
            } finally {
                setLoading(false);
            }
        };

        fetchJob();
    }, [id]);

    if (loading) {
        return <div className="um-state">Loading job details...</div>;
    }

    if (error || !job) {
        return (
            <div className="um-state">
                <div className="error-banner">{error || 'Job description not found.'}</div>
                <div className="form-actions jm-centered-actions">
                    <button type="button" className="btn-secondary jm-button-with-icon" onClick={() => navigate('/jobs')}>
                        <ArrowLeft size={16} aria-hidden="true" />
                        Back to Jobs
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="um-container">
            <JobPageHeader
                eyebrow="Hiring"
                title={job.title}
                description={`${job.department} | ${job.location}`}
                actions={(
                    <>
                        <button type="button" onClick={() => navigate('/jobs')} className="btn-secondary jm-button-with-icon">
                            <ArrowLeft size={16} aria-hidden="true" />
                            Back to Jobs
                        </button>
                        {canManageJobs ? (
                            <Link to={`/jobs/edit/${job._id}`} className="btn-primary jm-link-button jm-button-with-icon">
                                <SquarePen size={16} aria-hidden="true" />
                                Edit Job
                            </Link>
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
                            <span className="jm-detail-label">Status</span>
                            <JobStatusBadge isActive={job.is_active} />
                        </div>
                        <div className="jm-detail-item">
                            <span className="jm-detail-label">Experience</span>
                            <span className="jm-detail-value">
                                <BriefcaseBusiness size={16} aria-hidden="true" />
                                {job.experience_required}
                            </span>
                        </div>
                        <div className="jm-detail-item">
                            <span className="jm-detail-label">Department</span>
                            <span className="jm-detail-value">
                                <Building2 size={16} aria-hidden="true" />
                                {job.department}
                            </span>
                        </div>
                        <div className="jm-detail-item">
                            <span className="jm-detail-label">Location</span>
                            <span className="jm-detail-value">
                                <MapPin size={16} aria-hidden="true" />
                                {job.location}
                            </span>
                        </div>
                    </div>
                </section>

                <section className="form-card">
                    <div className="form-section-header">
                        <h2 className="form-section-title">Required Skills</h2>
                        <p className="form-section-copy">Skills currently expected for candidate evaluation.</p>
                    </div>

                    <div className="jm-skill-list jm-skill-list-spacious">
                        {(job.skills || []).map((skill) => (
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
                        {job.description}
                    </div>
                </section>
            </div>
        </div>
    );
};

export default JobDetailsScreen;
