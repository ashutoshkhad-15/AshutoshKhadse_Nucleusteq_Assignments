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

function showError(element, message) {
    if (!element) return;
    element.innerHTML = message;
    element.classList.add('active');
    element.style.animation = 'none';
    element.offsetHeight; // Triggers reflow
    element.style.animation = null;
}

function safeAddListener(id, event, handler) {
    const el = document.getElementById(id);
    if (el) {
        el.addEventListener(event, handler);
    } else {
        console.warn(`Element #${id} not found. Skipping event listener.`);
    }
}

function setupPasswordToggle(buttonId, inputId) {
    const toggleBtn = document.getElementById(buttonId);
    const passwordInput = document.getElementById(inputId);
    
    if (toggleBtn && passwordInput) {
        toggleBtn.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            toggleBtn.style.opacity = type === 'text' ? '1' : '0.6';
        });
    }
}

function initThemeToggle(toggleId) {
    const themeToggle = document.getElementById(toggleId);
    if (!themeToggle) return;

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

// Global Initialization for ALL pages
document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle('themeToggle');
    setupPasswordToggle('togglePassword', 'loginPassword');
    setupPasswordToggle('toggleRegPassword', 'registerPassword');
    
    if (typeof validateSession === 'function') {
        validateSession();
    }
});