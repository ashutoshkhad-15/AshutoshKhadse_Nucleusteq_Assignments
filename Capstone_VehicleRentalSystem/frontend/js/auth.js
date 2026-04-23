const API_BASE_URL = 'http://localhost:8080/api/auth';

/* THEME SWITCHER LOGIC */
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

/* FORMATTERS */
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

/* PASSWORD VISIBILITY TOGGLES */
// Login Page Toggle
const togglePasswordBtn = document.getElementById('togglePassword');
const loginPasswordInput = document.getElementById('loginPassword');

if (togglePasswordBtn && loginPasswordInput) {
    togglePasswordBtn.addEventListener('click', () => {
        const type = loginPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        loginPasswordInput.setAttribute('type', type);
        togglePasswordBtn.style.opacity = type === 'text' ? '1' : '0.6';
    });
}

// Registration Page Toggle
const toggleRegPasswordBtn = document.getElementById('toggleRegPassword');
const regPasswordInput = document.getElementById('registerPassword');

if (toggleRegPasswordBtn && regPasswordInput) {
    toggleRegPasswordBtn.addEventListener('click', () => {
        const type = regPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        regPasswordInput.setAttribute('type', type);
        toggleRegPasswordBtn.style.opacity = type === 'text' ? '1' : '0.6';
    });
}

/* LOGIN LOGIC & TOKEN STORAGE */
const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;

        // Handle both possible IDs safely
        const errorDiv = document.getElementById('loginErrorMessage') || document.getElementById('errorMessage');

        const submitBtn = document.getElementById('loginButton');

        //  Prevent crash if button not found
        if (submitBtn) {
            submitBtn.classList.add('loading');
            submitBtn.textContent = "Authenticating...";
        }

        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user_role', data.user.role);
                localStorage.setItem('user_name', data.user.firstName);

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
            // Prevent crash if button not found
            if (submitBtn) {
                submitBtn.classList.remove('loading');
                submitBtn.textContent = "Sign In";
            }
        }
    });
}

/* REGISTRATION LOGIC */
const registerForm = document.getElementById('registerForm');

if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const errorDiv = document.getElementById('registerErrorMessage');
        const submitBtn = document.getElementById('registerButton');

        const payload = {
            firstName: document.getElementById('registerFirstName').value.trim(),
            lastName: document.getElementById('registerLastName').value.trim(),
            email: document.getElementById('registerEmail').value.trim(),
            phoneNumber: document.getElementById('registerPhone').value.trim(),
            driversLicenseNumber: document.getElementById('registerLicense').value.trim(),
            password: document.getElementById('registerPassword').value
        };

        // Prevent crash if button not found
        if (submitBtn) {
            submitBtn.classList.add('loading');
            submitBtn.textContent = "Creating Profile...";
        }

        try {
            const response = await fetch(`${API_BASE_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                alert("🎉 Account created successfully! Please login.");
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
            if (submitBtn) {
                submitBtn.classList.remove('loading');
                submitBtn.textContent = "Join NexusFleet";
            }
        }
    });
}

/* HELPER FUNCTIONS */
function showError(element, message) {
    if (!element) return; 
    element.innerHTML = message;
    element.classList.add('active');

    element.style.animation = 'none';
    element.offsetHeight;
    element.style.animation = null;
}

/* LOGOUT FUNCTION */
function logout() {
    localStorage.clear();
    window.location.href = "index.html";
}