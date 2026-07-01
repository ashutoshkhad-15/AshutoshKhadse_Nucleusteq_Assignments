/**
 * Render the status badge used across the job module.
 *
 * @param {object} props - Component props.
 * @param {boolean} props.isActive - Whether the job is open.
 * @returns {JSX.Element} Status badge.
 */
const JobStatusBadge = ({ isActive }) => (
    <span className={`badge-status ${isActive ? 'active' : 'disabled'}`}>
        {isActive ? 'Open' : 'Closed'}
    </span>
);

export default JobStatusBadge;
