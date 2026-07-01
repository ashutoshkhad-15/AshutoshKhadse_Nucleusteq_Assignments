/**
 * Render the shared job module page header.
 *
 * @param {object} props - Component props.
 * @param {string} props.eyebrow - Small section label.
 * @param {string} props.title - Main page title.
 * @param {string} props.description - Supporting copy.
 * @param {React.ReactNode} [props.actions] - Optional header actions.
 * @returns {JSX.Element} Shared page header.
 */
const JobPageHeader = ({ eyebrow, title, description, actions }) => (
    <div className="um-header">
        <div className="um-title-group">
            <p className="um-eyebrow">{eyebrow}</p>
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
        {actions ? <div className="table-actions jm-header-actions">{actions}</div> : null}
    </div>
);

export default JobPageHeader;
