import { BadgeCheck, Pencil, Plus, Search, Users } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import useDebouncedValue from '../hooks/useDebouncedValue';
import { userService } from '../services/userService';
import '../styles/user-management.css';
import { getUserManagementErrorMessage, USER_ROLE_OPTIONS } from '../utils/userManagement';

/**
 * Displays the list of application users and provides
 * management actions for authorized administrators.
 *
 * @returns {JSX.Element} User management screen.
 */
const UserListScreen = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searching, setSearching] = useState(false);
    const [statusUpdatingId, setStatusUpdatingId] = useState('');
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');

    const [searchTerm, setSearchTerm] = useState('');
    const [filterRole, setFilterRole] = useState('ALL');
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

    const debouncedSearchTerm = useDebouncedValue(searchTerm, 800);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        if (!location.state?.successMessage) return;
        setSuccessMessage(location.state.successMessage);
        navigate(location.pathname, { replace: true });
    }, [location.pathname, location.state, navigate]);

    useEffect(() => {
        setCurrentPage(1);
    }, [debouncedSearchTerm, filterRole]);

    useEffect(() => {
        const controller = new AbortController();

        const loadUsers = async () => {
            const searchQuery = [debouncedSearchTerm.trim(), filterRole !== 'ALL' ? filterRole : '']
                .filter(Boolean)
                .join(' ');

            try {
                setError(null);
                if (loading && users.length === 0) {
                    setLoading(true);
                } else {
                    setSearching(true);
                }

                const data = await userService.getAllUsers(searchQuery, { signal: controller.signal });
                setUsers(data);
            } catch (err) {
                if (err?.name === 'CanceledError') {
                    return;
                }
                setError(getUserManagementErrorMessage(err, 'Failed to load users.'));
            } finally {
                setLoading(false);
                setSearching(false);
            }
        };

        loadUsers();

        return () => {
            controller.abort();
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [debouncedSearchTerm, filterRole]);

    const handleToggleStatus = async (userId, email, isActive) => {
        const nextStatus = !isActive;
        const actionLabel = nextStatus ? 'enable' : 'disable';
        const confirmationMessage = nextStatus
            ? `Are you sure you want to enable ${email}? They will regain access immediately.`
            : `Are you sure you want to disable ${email}? They will immediately lose access.`;

        if (!window.confirm(confirmationMessage)) return;

        try {
            setStatusUpdatingId(userId);
            await userService.updateUser(userId, { is_active: nextStatus });
            const searchQuery = [debouncedSearchTerm.trim(), filterRole !== 'ALL' ? filterRole : '']
                .filter(Boolean)
                .join(' ');
            const data = await userService.getAllUsers(searchQuery);
            setUsers(data);
            setSuccessMessage(`User ${email} ${actionLabel}d successfully.`);
            setError(null);
        } catch (err) {
            setError(getUserManagementErrorMessage(err, `Failed to ${actionLabel} user.`));
        } finally {
            setStatusUpdatingId('');
        }
    };

    const totalPages = Math.ceil(users.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const currentUsers = users.slice(startIndex, startIndex + itemsPerPage);

    const renderState = () => {
        if (loading) {
            return <div className="um-state">Loading users...</div>;
        }

        if (error) {
            return (
                <div className="um-state">
                    <div className="error-banner">{error}</div>
                    <button type="button" className="btn-secondary" onClick={() => window.location.reload()}>
                        Retry
                    </button>
                </div>
            );
        }

        return (
            <div className="table-card">
                {successMessage ? <div className="success-banner">{successMessage}</div> : null}

                <div className="um-toolbar">
                    <label className="visually-hidden" htmlFor="user-search-input">
                        Search users
                    </label>
                    <div className="search-input-wrapper">
                        <Search size={18} className="icon-inline" aria-hidden="true" />
                        <input
                            id="user-search-input"
                            type="text"
                            placeholder="Search by email or role"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="um-search-input"
                        />
                    </div>
                    <select
                        value={filterRole}
                        onChange={(e) => setFilterRole(e.target.value)}
                        className="um-filter-select"
                    >
                        <option value="ALL">All Roles</option>
                        {USER_ROLE_OPTIONS.map((option) => (
                            <option key={option.value} value={option.value}>
                                {option.label}
                            </option>
                        ))}
                    </select>
                </div>

                {searching ? (
                    <div className="empty-state">Searching users...</div>
                ) : currentUsers.length === 0 ? (
                    <div className="empty-state">
                        {searchTerm.trim() || filterRole !== 'ALL'
                            ? 'No users match your search criteria.'
                            : 'No users are available yet.'}
                    </div>
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
                                        <td className="um-user-email">
                                            <div className="user-email-cell">
                                                <Users size={16} className="icon-inline" aria-hidden="true" />
                                                {user.email}
                                            </div>
                                        </td>
                                        <td>
                                            <span className="badge-role">{user.role}</span>
                                        </td>
                                        <td>
                                            <span className={`badge-status ${user.is_active ? 'active' : 'disabled'}`}>
                                                <BadgeCheck size={14} className="icon-inline" aria-hidden="true" />
                                                {user.is_active ? 'Active' : 'Disabled'}
                                            </span>
                                        </td>
                                        <td className="align-right">
                                            <div className="table-actions">
                                                <Link to={`/users/edit/${user._id}`} className="action-edit">
                                                    <Pencil size={14} className="icon-inline" aria-hidden="true" />
                                                    Edit
                                                </Link>
                                                <button
                                                    onClick={() => handleToggleStatus(user._id, user.email, user.is_active)}
                                                    disabled={statusUpdatingId === user._id || user.email === 'admin@nucleusteq.com'}
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

                        {totalPages > 1 && (
                            <div className="um-pagination">
                                <span className="pagination-info">
                                    Showing {startIndex + 1} to {Math.min(startIndex + itemsPerPage, users.length)} of {users.length} users
                                </span>
                                <div className="pagination-buttons">
                                    <button
                                        onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                                        disabled={currentPage === 1}
                                        className="btn-page"
                                    >
                                        Previous
                                    </button>
                                    <button
                                        onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
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
        );
    };

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Administration</p>
                    <h1>User Management</h1>
                    <p>Manage system access, role assignment, and account status for internal users.</p>
                </div>
                <button
                    type="button"
                    onClick={() => navigate('/users/create')}
                    className="btn-primary btn-icon"
                >
                    <Plus size={18} className="icon-inline" aria-hidden="true" />
                    Create User
                </button>
            </div>
            {renderState()}
        </div>
    );
};

export default UserListScreen;
