import { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import useDebouncedValue from '../hooks/useDebouncedValue';
import { DEFAULT_ADMIN_EMAIL } from '../constants/userConstants';
import { userService } from '../services/userService';
import '../styles/user-management.css';
import { formatUserRange, getUserManagementErrorMessage, isProtectedUser } from '../utils/userManagement';
import { loadUserList } from '../utils/pageLoaders';
import { getListPagination, getListRows, isCanceledRequest } from '../utils/listPage';

/**
 * Displays the user management list for administrators.
 */
const UserListScreen = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searching, setSearching] = useState(false);
    const [statusUpdatingId, setStatusUpdatingId] = useState('');
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');
    const [searchTerm, setSearchTerm] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;
    const [pagination, setPagination] = useState({ page: 1, limit: 10, total_items: 0, total_pages: 1 });
    const debouncedSearchTerm = useDebouncedValue(searchTerm, 800);
    const navigate = useNavigate();
    const location = useLocation();
    const requestSearch = debouncedSearchTerm.trim();

    useEffect(() => {
        if (!location.state?.successMessage) return;
        setSuccessMessage(location.state.successMessage);
        navigate(location.pathname, { replace: true });
    }, [location.pathname, location.state, navigate]);

    useEffect(() => setCurrentPage(1), [debouncedSearchTerm]);

    useEffect(() => {
        const controller = new AbortController();
        setError(null);
        if (loading && users.length === 0) setLoading(true);
        else setSearching(true);
            loadUserList(requestSearch, currentPage, itemsPerPage, controller.signal)
                .then((response) => {
                    setUsers(getListRows(response));
                    setPagination(getListPagination(response));
                })
                .catch((err) => {
                    if (!isCanceledRequest(err)) setError(getUserManagementErrorMessage(err, 'Failed to load users.'));
                })
            .finally(() => {
                setLoading(false);
                setSearching(false);
            });
        return () => controller.abort();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [requestSearch, currentPage, itemsPerPage]);

    const handleToggleStatus = async (userId, email, isActive) => {
        const nextStatus = !isActive;
        const actionLabel = nextStatus ? 'enable' : 'disable';

        if (!window.confirm(nextStatus ? `Enable ${email}?` : `Disable ${email}?`)) return;

        try {
            setStatusUpdatingId(userId);
            await userService.updateUser(userId, { is_active: nextStatus });
            const response = await loadUserList(requestSearch, currentPage, itemsPerPage);
            setUsers(getListRows(response));
            setPagination(getListPagination(response));
            setSuccessMessage(`User ${email} ${actionLabel}d successfully.`);
            setError(null);
        } catch (err) {
            setError(getUserManagementErrorMessage(err, `Failed to ${actionLabel} user.`));
        } finally {
            setStatusUpdatingId('');
        }
    };

    if (loading) return <div className="um-state">Loading users...</div>;

    return (
        <div className="um-container">
            <div className="um-header">
                <div className="um-title-group">
                    <p className="um-eyebrow">Administration</p>
                    <h1>User Management</h1>
                    <p>Manage system access, role assignment, and account status for internal users.</p>
                </div>
                <button type="button" onClick={() => navigate('/users/create')} className="btn-primary">Create User</button>
            </div>

            <div className="table-card">
                {successMessage ? <div className="success-banner">{successMessage}</div> : null}
                {error ? <div className="error-banner">{error}</div> : null}
                <div className="um-toolbar">
                    <input id="user-search-input" type="text" placeholder="Search by name, email, or role" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="um-search-input" />
                </div>
                {searching ? <div className="empty-state">Searching users...</div> : users.length === 0 ? <div className="empty-state">{searchTerm.trim() ? 'No users match your search criteria.' : 'No users are available yet.'}</div> : (
                    <>
                        <table className="um-table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Status</th>
                                    <th className="align-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.map((user) => (
                                    <tr key={user._id}>
                                        <td data-label="Name">{user.name}</td>
                                        <td data-label="Email">{user.email}</td>
                                        <td data-label="Role">{user.role}</td>
                                        <td data-label="Status">{user.is_active ? 'Active' : 'Disabled'}</td>
                                        <td className="align-right" data-label="Actions">
                                            <div className="table-actions">
                                                {isProtectedUser(user) ? <button type="button" className="btn-secondary" disabled>Edit</button> : <Link to={`/users/edit/${user._id}`} className="btn-secondary">Edit</Link>}
                                                <button onClick={() => handleToggleStatus(user._id, user.email, user.is_active)} disabled={statusUpdatingId === user._id || user.email === DEFAULT_ADMIN_EMAIL} className="btn-secondary">
                                                    {user.is_active ? 'Disable' : 'Enable'}
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {pagination.total_pages > 1 ? (
                            <div className="um-pagination">
                                <span className="pagination-info">Showing {formatUserRange(pagination.page || currentPage, pagination.limit || itemsPerPage, users.length)} of {pagination.total_items} users</span>
                                <div className="pagination-buttons">
                                    <button onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))} disabled={currentPage === 1} className="btn-page">Previous</button>
                                    <button onClick={() => setCurrentPage((prev) => Math.min(prev + 1, pagination.total_pages || 1))} disabled={currentPage === (pagination.total_pages || 1)} className="btn-page">Next</button>
                                </div>
                            </div>
                        ) : null}
                    </>
                )}
            </div>
        </div>
    );
};

export default UserListScreen;
