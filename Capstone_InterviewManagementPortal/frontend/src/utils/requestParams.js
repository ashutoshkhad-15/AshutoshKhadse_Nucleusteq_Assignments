// Provides reusable function to append optional query parameters

export const withSearchParam = (search, config = {}) => {
    const params = { ...(config.params || {}) };
    if (search?.trim()) params.search = search.trim();
    return { ...config, params };
};

