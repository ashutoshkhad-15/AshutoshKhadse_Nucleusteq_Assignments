export const DEFAULT_PAGINATION = {
    page: 1,
    limit: 10,
    total_items: 0,
    total_pages: 1,
};

export const isCanceledRequest = (error) => error?.name === 'CanceledError';

export const getListRows = (response) => (Array.isArray(response?.data) ? response.data : []);

export const getListPagination = (response) => response?.meta || DEFAULT_PAGINATION;

export const getPaginationRange = (pagination, currentPage, itemsPerPage, itemCount) => {
    if (!itemCount) {
        return [0, 0];
    }

    const page = pagination.page || currentPage;
    const limit = pagination.limit || itemsPerPage;
    const start = (page - 1) * limit + 1;

    return [start, start + itemCount - 1];
};
