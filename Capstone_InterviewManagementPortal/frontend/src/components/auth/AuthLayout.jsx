/**
 * Shared split-screen layout for authentication pages.
 *
 * @param {object} props - Component props.
 * @param {string} props.title - Heading shown in the brand panel.
 * @param {string} props.tagline - Supporting text shown in the brand panel.
 * @param {React.ReactNode} props.children - Form content displayed in the right panel.
 * @returns {JSX.Element} Authentication page layout.
 */
const AuthLayout = ({ title, tagline, children }) => {
    return (
        <div className="portal-layout">
            <div className="portal-brand">
                <div className="portal-brand-content">
                    <div className="portal-logo-container">
                        <img src="/logo.png" alt="NucleusTeq Mark" className="portal-logo-img" />
                        <div className="portal-brand-name">NucleusTeq</div>
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
