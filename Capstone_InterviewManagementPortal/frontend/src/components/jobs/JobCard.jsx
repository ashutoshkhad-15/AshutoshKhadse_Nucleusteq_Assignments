import { Link } from 'react-router-dom';

/**
 * Renders a simple job summary card.
 */
const JobCard = ({ job, canManageJobs }) => {
    const skills = Array.isArray(job.requiredSkills) ? job.requiredSkills : [];

    return (
        <article className="jm-job-card">
            <h2 className="jm-job-card-title">{job.jobTitle}</h2>
            <p className="jm-job-card-copy">{job.jobRole}</p>
            <p className="jm-job-card-summary">{job.jobDetails}</p>
            <p className="jm-job-card-copy">Experience: {job.experienceRequired}</p>
            <p className="jm-job-card-copy">Type: {job.employmentType}</p>
            <p className="jm-job-card-copy">Location: {job.location}</p>
            <div className="jm-skill-list">
                {skills.slice(0, 5).map((skill) => (
                    <span key={skill} className="jm-skill-pill">{skill}</span>
                ))}
            </div>
            <div className="jm-card-actions">
                <Link to={`/jobs/${job._id}`} className="btn-secondary">View</Link>
                {canManageJobs ? <Link to={`/jobs/edit/${job._id}`} className="btn-secondary">Edit</Link> : null}
            </div>
        </article>
    );
};

export default JobCard;
