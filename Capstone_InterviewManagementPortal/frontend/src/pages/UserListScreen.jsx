import { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { userService } from '../services/userService';
import { getUserManagementErrorMessage } from '../utils/userManagement';
import '../styles/user-management.css';

/**
 * Displays the list of application users and provides
 * management actions for authorized administrators.
 *
 * @returns {JSX.Element} User management screen.
 */
const UserListScreen = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');

    // State used for client-side searching, filtering, and pagination.
    const [searchTerm, setSearchTerm] = useState('');
    const [filterRole, setFilterRole] = useState('ALL');
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        loadUsers();
    }, []);

    useEffect(() => {
        if (!location.state?.successMessage) return;
        setSuccessMessage(location.state.successMessage);
        navigate(location.pathname, { replace: true });
    }, [location.pathname, location.state, navigate]);

    // Reset pagination whenever the visible dataset changes.
    useEffect(() => {
        setCurrentPage(1);
    }, [searchTerm, filterRole]);

    /**
     * Retrieves all users from the backend and updates the
     * component state with the latest data.
     *
     * Displays an appropriate error message if the request fails.
     *
     * @returns {Promise<void>}
     */
    const loadUsers = async () => {
        try {
            setLoading(true);
            const data = await userService.getAllUsers();
            setUsers(data);
            setError(null);
        } catch (err) {
            setError(getUserManagementErrorMessage(err, 'Failed to load users.'));
        } finally {
            setLoading(false);
        }
    };

    /**
     * Enables or disables a user account after confirmation.
     *
     * Refreshes the user list on success and displays the
     * appropriate success or error message.
     *
     * @param {string} userId User identifier.
     * @param {string} email User email address.
     * @param {boolean} isActive Current account status.
     * @returns {Promise<void>}
     */
    const handleToggleStatus = async (userId, email, isActive) => {
        const nextStatus = !isActive;
        const actionLabel = nextStatus ? 'enable' : 'disable';
        const confirmationMessage = nextStatus
            ? `Are you sure you want to enable ${email}? They will regain access immediately.`
            : `Are you sure you want to disable ${email}? They will immediately lose access.`;

        if (!window.confirm(confirmationMessage)) return;

        try {
            await userService.updateUser(userId, { is_active: nextStatus });
            await loadUsers();
            setSuccessMessage(`User ${email} ${actionLabel}d successfully.`);
            setError(null);
        } catch (err) {
            setError(getUserManagementErrorMessage(err, `Failed to ${actionLabel} user.`));
        }
    };

    /**
     * Filters the user list based on the search term and selected role.
     *
     * @returns {Array} Filtered array of users.
     */
    const filteredUsers = users.filter(user => {
        const matchesSearch = user.email.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesRole = filterRole === 'ALL' || user.role === filterRole;
        return matchesSearch && matchesRole;
    });

    const totalPages = Math.ceil(filteredUsers.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const currentUsers = filteredUsers.slice(startIndex, startIndex + itemsPerPage);

    if (loading) {
        return <div className="um-state">Loading users...</div>;
    }

    if (error) {
        return (
            <div className="um-state">
                <div className="error-banner">{error}</div>
                <button type="button" className="btn-secondary" onClick={loadUsers}>
                    Retry
                </button>
            </div>
        );
    }

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Administration</p>
                    <h1>User Management</h1>
                    <p>Manage system access, role assignment, and account status for internal users.</p>
                </div>
                <button
                    onClick={() => navigate('/users/create')}
                    className="btn-primary"
                >
                    Create User
                </button>
            </div>

            <div className="table-card">
                {successMessage ? <div className="success-banner">{successMessage}</div> : null}

                {/* Search and filtering controls. */}
                <div className="um-toolbar">
                    <input
                        type="text"
                        placeholder="Search by email..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="um-search-input"
                    />
                    <select
                        value={filterRole}
                        onChange={(e) => setFilterRole(e.target.value)}
                        className="um-filter-select"
                    >
                        <option value="ALL">All Roles</option>
                        <option value="ADMIN">Admin</option>
                        <option value="HR">HR</option>
                        <option value="INTERVIEWER">Interviewer</option>
                    </select>
                </div>

                {filteredUsers.length === 0 ? (
                    <div className="empty-state">No users match your search criteria.</div>
                ) : (
                    <>
                        <table className="um-table">
                            <thead>
                                <tr>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Status</th>
                                    <th className="align-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {currentUsers.map((user) => (
                                    <tr key={user._id}>
                                        <td className="um-user-email">{user.email}</td>
                                        <td>
                                            <span className="badge-role">{user.role}</span>
                                        </td>
                                        <td>
                                            <span className={`badge-status ${user.is_active ? 'active' : 'disabled'}`}>
                                                {user.is_active ? 'Active' : 'Disabled'}
                                            </span>
                                        </td>
                                        <td className="align-right">
                                            <div className="table-actions">
                                                <Link to={`/users/edit/${user._id}`} className="action-edit">
                                                    Edit
                                                </Link>
                                                <button
                                                    onClick={() => handleToggleStatus(user._id, user.email, user.is_active)}
                                                    disabled={user.email === 'admin@nucleusteq.com'}
                                                    className={user.is_active ? 'action-disable' : 'action-enable'}
                                                >
                                                    {user.is_active ? 'Disable' : 'Enable'}
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {/* Render pagination only when multiple pages are available. */}
                        {totalPages > 1 && (
                            <div className="um-pagination">
                                <span className="pagination-info">
                                    Showing {startIndex + 1} to {Math.min(startIndex + itemsPerPage, filteredUsers.length)} of {filteredUsers.length} users
                                </span>
                                <div className="pagination-buttons">
                                    <button
                                        onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                                        disabled={currentPage === 1}
                                        className="btn-page"
                                    >
                                        Previous
                                    </button>
                                    <button
                                        onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                                        disabled={currentPage === totalPages}
                                        className="btn-page"
                                    >
                                        Next
                                    </button>
                                </div>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
};

export default UserListScreen;