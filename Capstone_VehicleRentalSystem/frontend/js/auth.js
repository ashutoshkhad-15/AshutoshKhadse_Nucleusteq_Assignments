
const API_BASE_URL = 'http://localhost:8080/api/auth';

/* THEME SWITCHER LOGIC */
const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
    // Check if user previously selected light mode
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
        const errorDiv = document.getElementById('errorMessage');
        const submitBtn = document.getElementById('loginButton');

        // UX: Disable button and show loading state
        submitBtn.classList.add('loading');
        submitBtn.textContent = "Authenticating...";

        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                // SUCCESS: Store the JWT and User info securely
                localStorage.setItem('token', data.token);
                localStorage.setItem('user_role', data.user.role);
                localStorage.setItem('user_name', data.user.firstName);

                // ROUTING: Send the authenticated user to the protected dashboard
                window.location.href = 'dashboard.html';
            } else {
                showError(errorDiv, data.error || "Authentication failed. Please check your credentials.");
            }
        } catch (error) {
            showError(errorDiv, "Server connection error. Is the NexusFleet backend running?");
        } finally {
            // UX: Restore button state
            submitBtn.classList.remove('loading');
            submitBtn.textContent = "Sign In";
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

        // Construct the exact DTO payload Spring Boot expects
        const payload = {
            firstName: document.getElementById('registerFirstName').value.trim(),
            lastName: document.getElementById('registerLastName').value.trim(),
            email: document.getElementById('registerEmail').value.trim(),
            phoneNumber: document.getElementById('registerPhone').value.trim(),
            driversLicenseNumber: document.getElementById('registerLicense').value.trim(),
            password: document.getElementById('registerPassword').value
        };

        // UX: Disable button
        submitBtn.classList.add('loading');
        submitBtn.textContent = "Creating Profile...";

        try {
            const response = await fetch(`${API_BASE_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                // SUCCESS: Alert user and route back to login
                alert('Welcome to NexusFleet! Your account has been created. Please sign in.');
                window.location.href = 'index.html';
            } else {
                showError(errorDiv, data.error || "Registration failed. Please check your information.");
            }
        } catch (error) {
            showError(errorDiv, "Server connection error. Please try again later.");
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.textContent = "Join NexusFleet";
        }
    });
}

/* HELPER FUNCTIONS */
function showError(element, message) {
    element.textContent = message;
    element.classList.add('active');

    // Trigger CSS "shake" reflow
    element.style.animation = 'none';
    element.offsetHeight;
    element.style.animation = null;
}