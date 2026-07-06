/**
 * Renders the shared heading for job pages.
 */
const JobPageHeader = ({ eyebrow, title, description, actions }) => (
    <div className="um-header">
        <div className="um-title-group">
            <p className="um-eyebrow">{eyebrow}</p>
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
        {actions ? <div>{actions}</div> : null}
    </div>
);

export default JobPageHeader;
