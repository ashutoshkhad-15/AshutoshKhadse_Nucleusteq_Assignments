const API_BASE_URL = 'http://localhost:8080/api';

function getAuthHeaders() {
    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
}

function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}

async function apiFetch(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
    options.headers = { ...getAuthHeaders(), ...options.headers };
    
    try {
        const response = await fetch(url, options);
        // Don't force logout if we get 401 on the login/register pages
        if (response.status === 401) {
            const isAuthPage = window.location.pathname.includes('index.html') || window.location.pathname.includes('register.html');
            if (!isAuthPage) {
                console.warn("Session expired. Forcing logout.");
                logout();
            }
        }
        return response;
    } catch (error) {
        console.error("API Fetch Error:", error);
        throw error;
    }
}

async function validateSession() {
    const token = localStorage.getItem('token');
    const currentPage = window.location.pathname;
    const isAuthPage = currentPage.includes('index.html') || currentPage.includes('register.html') || currentPage.endsWith('/');

    if (!token) {
        if (!isAuthPage) logout();
        return;
    }

    if (!isAuthPage) {
        try {
            const response = await apiFetch('/auth/me', { method: 'GET' });
            if (response.ok) {
                const userData = await response.json();
                localStorage.setItem('user_role', userData.role);
                localStorage.setItem('user_name', userData.firstName);
            } else {
                logout();
            }
        } catch (error) {
            console.error("Failed to validate session.", error);
        }
    }
}