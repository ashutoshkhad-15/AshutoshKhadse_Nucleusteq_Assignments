// Login Logic
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const emailInput = document.getElementById('loginEmail');
        const passwordInput = document.getElementById('loginPassword');
        const errorDiv = document.getElementById('loginErrorMessage') || document.getElementById('errorMessage');
        const submitBtn = document.getElementById('loginButton');

        if (submitBtn) {
            submitBtn.classList.add('loading');
            submitBtn.textContent = "Authenticating...";
        }
        emailInput.disabled = true;
        passwordInput.disabled = true;

        try {
            const response = await apiFetch('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ 
                    email: emailInput.value.trim(), 
                    password: passwordInput.value 
                })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('user_role', data.user.role);
                localStorage.setItem('user_name', data.user.firstName);
                localStorage.setItem('user_email', data.user.email);
                window.location.href = 'dashboard.html';
            } else {
                showError(errorDiv, data.errors ? formatValidationErrors(data.errors) : (data.error || "Invalid credentials"));
            }
        } catch (error) {
            showError(errorDiv, "Server connection error.");
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

// Registration Logic 
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

        const inputs = [firstNameInput, lastNameInput, emailInput, phoneInput, licenseInput, passwordInput];
        inputs.forEach(input => input.disabled = true);

        try {
            const response = await apiFetch('/auth/register', {
                method: 'POST',
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                alert("Account created successfully! Please login.");
                window.location.href = "index.html";
            } else {
                showError(errorDiv, data.errors ? formatValidationErrors(data.errors) : (data.message || "Registration failed"));
            }
        } catch (error) {
            showError(errorDiv, "Server connection error.");
        } finally {
            inputs.forEach(input => input.disabled = false);
            if (submitBtn) {
                submitBtn.classList.remove('loading');
                submitBtn.textContent = "Join NexusFleet";
            }
        }
    });
}