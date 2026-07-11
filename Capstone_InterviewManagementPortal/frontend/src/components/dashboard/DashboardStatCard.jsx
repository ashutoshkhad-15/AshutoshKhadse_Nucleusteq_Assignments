/**
 * Render a small dashboard statistic card.
 */
const DashboardStatCard = ({ label, value }) => (
    <div className="form-card dashboard-stat-card">
        <h2 className="form-section-title">{label}</h2>
        <p className="dashboard-stat-value">{value}</p>
    </div>
);

export default DashboardStatCard;
