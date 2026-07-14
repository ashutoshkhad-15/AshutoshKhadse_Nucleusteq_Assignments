/**
 * Shared split-screen layout for authentication pages.
 */
const AuthLayout = ({ title, tagline, children }) => {
    return (
        <div className="portal-layout">
            <div className="portal-brand">
                <div className="portal-brand-content">
                    <div className="portal-logo-container">
                        <img src="/logo.png" alt="LOGO" className="portal-logo-img" />
                        <div className="portal-brand-name">TalentFlow</div>
                    </div>

                    <h1 className="portal-logo-text">{title}</h1>
                    <p className="portal-tagline">{tagline}</p>
                </div>
            </div>

            <div className="portal-form-wrapper">
                <div className="portal-form-container">
                    {children}
                </div>
            </div>
        </div>
    );
};

export default AuthLayout;
