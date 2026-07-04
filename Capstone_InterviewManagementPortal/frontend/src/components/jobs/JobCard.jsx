import { Eye, SquarePen } from 'lucide-react';
import { Link } from 'react-router-dom';

/**
 * Render a single job card in the listing grid.
 *
 * @param {object} props - Component props.
 * @param {{ _id: string, jobTitle: string, jobRole: string, jobDetails: string, requiredSkills?: string[], experienceRequired: string, employmentType: string, location: string }} props.job - Job record to display.
 * @param {boolean} props.canManageJobs - Whether the current role can edit jobs.
 * @returns {JSX.Element} Job card.
 */
const JobCard = ({ job, canManageJobs }) => {
    const skills = Array.isArray(job.requiredSkills) ? job.requiredSkills : [];

    return (
        <article className="jm-job-card">
            <div className="jm-job-card-top">
                <div>
                    <h2 className="jm-job-card-title">{job.jobTitle}</h2>
                    <p className="jm-job-card-copy">{job.jobRole}</p>
                </div>
            </div>

            <div className="jm-job-card-meta">
                <div className="jm-job-chip">
                    <span className="jm-detail-label">Experience</span>
                    <span className="jm-job-chip-value">{job.experienceRequired}</span>
                </div>
                <div className="jm-job-chip">
                    <span className="jm-detail-label">Type</span>
                    <span className="jm-job-chip-value">{job.employmentType}</span>
                </div>
                <div className="jm-job-chip">
                    <span className="jm-detail-label">Location</span>
                    <span className="jm-job-chip-value">{job.location}</span>
                </div>
            </div>

            <div className="jm-skill-list jm-skill-list-spacious">
                {skills.slice(0, 5).map((skill) => (
                    <span key={skill} className="jm-skill-pill">{skill}</span>
                ))}
                {skills.length > 5 ? <span className="jm-skill-pill jm-skill-pill-muted">+{skills.length - 5} more</span> : null}
            </div>

            <p className="jm-job-card-summary">{job.jobDetails}</p>

            <div className="jm-card-actions">
                <Link to={`/jobs/${job._id}`} className="action-edit jm-action-button">
                    <Eye size={14} className="icon-inline" aria-hidden="true" />
                    <span>View</span>
                </Link>
                {canManageJobs ? (
                    <Link to={`/jobs/edit/${job._id}`} className="action-edit jm-action-button">
                        <SquarePen size={14} className="icon-inline" aria-hidden="true" />
                        <span>Edit</span>
                    </Link>
                ) : null}
            </div>
        </article>
    );
};

export default JobCard;
