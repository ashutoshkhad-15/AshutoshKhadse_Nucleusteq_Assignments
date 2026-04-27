const AUTH_API_URL = 'http://localhost:8080/api/auth';

const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
    if (localStorage.getItem('theme') === 'light') {
        document.body.classList.replace('dark-theme', 'light-theme');
        themeToggle.checked = true;
    }

    themeToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            document.body.classList.replace('dark-theme', 'light-theme');
            localStorage.setItem('theme', 'light');
        } else {
            document.body.classList.replace('light-theme', 'dark-theme');
            localStorage.setItem('theme', 'dark');
        }
    });
}

function formatValidationErrors(errors) {
    return Object.entries(errors)
        .map(([field, message]) => `❌ ${formatFieldName(field)}: ${message}`)
        .join("<br>");
}

function formatFieldName(field) {
    return field
        .replace(/([A-Z])/g, " $1")
        .replace(/^./, str => str.toUpperCase());
}

const togglePasswordBtn = document.getElementById('togglePassword');
const loginPasswordInput = document.getElementById('loginPassword');
if (togglePasswordBtn && loginPasswordInput) {
    togglePasswordBtn.addEventListener('click', () => {
        const type = loginPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        loginPasswordInput.setAttribute('type', type);
        togglePasswordBtn.style.opacity = type === 'text' ? '1' : '0.6';
    });
}

const toggleRegPasswordBtn = document.getElementById('toggleRegPassword');
const regPasswordInput = document.getElementById('registerPassword');
if (toggleRegPasswordBtn && regPasswordInput) {
    toggleRegPasswordBtn.addEventListener('click', () => {
        const type = regPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        regPasswordInput.setAttribute('type', type);
        toggleRegPasswordBtn.style.opacity = type === 'text' ? '1' : '0.6';
    });
}

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const emailInput = document.getElementById('loginEmail');
        const passwordInput = document.getElementById('loginPassword');
        const errorDiv = document.getElementById('loginErrorMessage') || document.getElementById('errorMessage');
        const submitBtn = document.getElementById('loginButton');

        const email = emailInput.value.trim();
        const password = passwordInput.value;

        if (submitBtn) {
            submitBtn.classList.add('loading');
            submitBtn.textContent = "Authenticating...";
        }

        emailInput.disabled = true;
        passwordInput.disabled = true;

        try {
            const response = await fetch(`${AUTH_API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user_role', data.user.role);
                localStorage.setItem('user_name', data.user.firstName);
                localStorage.setItem('user_email', data.user.email);
                window.location.href = 'dashboard.html';
            } else {
                if (data.errors) {
                    showError(errorDiv, formatValidationErrors(data.errors));
                } else {
                    showError(errorDiv, data.error || data.message || "Invalid email or password");
                }
            }
        } catch (error) {
            showError(errorDiv, "Server connection error. Is backend running?");
        } finally {
            emailInput.disabled = false;
            passwordInput.disabled = false;
            if (submitBtn) {
                submitBtn.classList.remove('loading');
                submitBtn.textContent = "Sign In";
            }
        }
    });
}

const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const errorDiv = document.getElementById('registerErrorMessage');
        const submitBtn = document.getElementById('registerButton');

        const firstNameInput = document.getElementById('registerFirstName');
        const lastNameInput = document.getElementById('registerLastName');
        const emailInput = document.getElementById('registerEmail');
        const phoneInput = document.getElementById('registerPhone');
        const licenseInput = document.getElementById('registerLicense');
        const passwordInput = document.getElementById('registerPassword');

        const payload = {
            firstName: firstNameInput.value.trim(),
            lastName: lastNameInput.value.trim(),
            email: emailInput.value.trim(),
            phoneNumber: phoneInput.value.trim(),
            driversLicenseNumber: licenseInput.value.trim(),
            password: passwordInput.value
        };

        if (submitBtn) {
            submitBtn.classList.add('loading');
            submitBtn.textContent = "Creating Profile...";
        }

        firstNameInput.disabled = true;
        lastNameInput.disabled = true;
        emailInput.disabled = true;
        phoneInput.disabled = true;
        licenseInput.disabled = true;
        passwordInput.disabled = true;

        try {
            const response = await fetch(`${AUTH_API_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                alert(" Account created successfully! Please login.");
                window.location.href = "index.html";
            } else {
                if (data.errors) {
                    showError(errorDiv, formatValidationErrors(data.errors));
                } else {
                    showError(errorDiv, data.message || "Registration failed");
                }
            }
        } catch (error) {
            showError(errorDiv, "Server connection error. Please try again.");
        } finally {
            firstNameInput.disabled = false;
            lastNameInput.disabled = false;
            emailInput.disabled = false;
            phoneInput.disabled = false;
            licenseInput.disabled = false;
            passwordInput.disabled = false;

            if (submitBtn) {
                submitBtn.classList.remove('loading');
                submitBtn.textContent = "Join NexusFleet";
            }
        }
    });
}

function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
    };
}

async function apiFetch(url, options = {}) {
    options.headers = { ...getAuthHeaders(), ...options.headers };
    try {
        const response = await fetch(url, options);
        if (response.status === 401) {
            console.warn("Session expired. Forcing logout.");
            logout();
            throw new Error("Session expired");
        }
        return response;
    } catch (error) {
        console.error("API Fetch Error:", error);
        throw error;
    }
}

async function validateSession() {
    const token = localStorage.getItem('token');
    if (!token) {
        logout();
        return;
    }
    try {
        const response = await fetch('http://localhost:8080/api/auth/me', {
            method: 'GET',
            headers: getAuthHeaders()
        });
        if (response.ok) {
            const userData = await response.json();
            localStorage.setItem('user_role', userData.role);
            localStorage.setItem('user_name', userData.firstName);
        } else {
            logout();
        }
    } catch (error) {
        console.error("Failed to validate session. Server might be down.", error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname;
    if (!currentPage.includes('index.html') && !currentPage.includes('register.html')) {
        validateSession();
    }
});

function showError(element, message) {
    if (!element) return;
    element.innerHTML = message;
    element.classList.add('active');
    element.style.animation = 'none';
    element.offsetHeight;
    element.style.animation = null;
}

function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}