const DASHBOARD_API_URL = 'http://localhost:8080/api';

let currentVehicles = [];
let currentBookings = [];
let selectedVehicleId = null;
const userRole = localStorage.getItem('user_role');
const userName = localStorage.getItem('user_name');

// Calendar Instances
let startDatePicker = null;
let endDatePicker = null;
let filterStartDatePicker = null; // New for dashboard filters
let filterEndDatePicker = null;   // New for dashboard filters

// Helper function to safely attach events
function safeAddListener(id, event, handler) {
    const el = document.getElementById(id);
    if (el) {
        el.addEventListener(event, handler);
    } else {
        console.warn(`Element #${id} not found. Skipping event listener.`);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('welcomeMessage').textContent = userName || 'Driver';
    const badge = document.getElementById('roleBadge');
    badge.textContent = userRole === 'ADMIN' ? 'Admin Portal' : 'Member Portal';
    badge.style.background = userRole === 'ADMIN' ? '#ef4444' : 'var(--accent)';

    if (userRole === 'ADMIN') {
        document.getElementById('adminAddVehicleBtn').style.display = 'block';
        document.getElementById('navBookingsBtn').textContent = 'Bookings';
        const statusDropdown = document.getElementById('filterStatus');
        if (statusDropdown) {
            const retiredOption = document.createElement('option');
            retiredOption.value = 'RETIRED';
            retiredOption.textContent = 'Retired';
            statusDropdown.appendChild(retiredOption);
        }
    } else {
        document.getElementById('navBookingsBtn').textContent = 'My Bookings';
    }

    filterStartDatePicker = flatpickr("#filterStartDate", {
        minDate: "today",
        dateFormat: "Y-m-d",
        disableMobile: true,
        onChange: function (selectedDates, dateStr) {
            if (filterEndDatePicker) filterEndDatePicker.set('minDate', dateStr);
        }
    });

    filterEndDatePicker = flatpickr("#filterEndDate", {
        minDate: "today",
        dateFormat: "Y-m-d",
        disableMobile: true
    });

    setupEventListeners();
    loadCatalog();
});

function setupEventListeners() {
    safeAddListener('navCatalogBtn', 'click', showCatalogView);
    safeAddListener('navBookingsBtn', 'click', showBookingsView);
    safeAddListener('backToCatalogBtn', 'click', showCatalogView);
    safeAddListener('logoutBtn', 'click', logout);

    safeAddListener('applyFiltersBtn', 'click', applyFilters);
    safeAddListener('clearFiltersBtn', 'click', () => {
        document.getElementById('filterType').value = '';
        document.getElementById('filterStatus').value = '';

        if (filterStartDatePicker) filterStartDatePicker.clear();
        if (filterEndDatePicker) {
            filterEndDatePicker.clear();
            filterEndDatePicker.set('minDate', 'today');
        }

        loadCatalog();
    });

    safeAddListener('closeBookingModalBtn', 'click', () => {
        document.getElementById('bookingModalOverlay').style.display = 'none';
    });
    safeAddListener('bookingForm', 'submit', handleBookingSubmit);
    safeAddListener('closeReviewModalBtn', 'click', () => {
        document.getElementById('reviewModalOverlay').style.display = 'none';
    });
    safeAddListener('reviewForm', 'submit', handleReviewSubmit);
    safeAddListener('bookingStatusFilter', 'change', filterBookings);

    if (userRole === 'ADMIN') {
        safeAddListener('adminAddVehicleBtn', 'click', () => {
            const overlay = document.getElementById('addModalOverlay');
            if (overlay) overlay.style.display = 'flex';
        });

        safeAddListener('closeAddModalBtn', 'click', () => {
            document.getElementById('addModalOverlay').style.display = 'none';
        });
        safeAddListener('cancelAddBtn', 'click', () => {
            document.getElementById('addModalOverlay').style.display = 'none';
        });
        safeAddListener('addVehicleForm', 'submit', handleAddVehicle);

        safeAddListener('closeModalBtn', 'click', () => {
            document.getElementById('editModalOverlay').style.display = 'none';
        });
        safeAddListener('cancelEditBtn', 'click', () => {
            document.getElementById('editModalOverlay').style.display = 'none';
        });
        safeAddListener('editVehicleForm', 'submit', handleEditVehicle);
    }
}

function showCatalogView() {
    document.getElementById('catalogView').style.display = 'block';
    document.getElementById('detailView').style.display = 'none';
    document.getElementById('bookingsView').style.display = 'none';

    document.getElementById('navCatalogBtn').classList.add('active');
    document.getElementById('navBookingsBtn').classList.remove('active');
    loadCatalog();
}

function showBookingsView() {
    document.getElementById('catalogView').style.display = 'none';
    document.getElementById('detailView').style.display = 'none';
    document.getElementById('bookingsView').style.display = 'flex';

    document.getElementById('navCatalogBtn').classList.remove('active');
    document.getElementById('navBookingsBtn').classList.add('active');
    loadBookings();
}

function showDetailView(vehicleId) {
    document.getElementById('catalogView').style.display = 'none';
    document.getElementById('bookingsView').style.display = 'none';
    document.getElementById('detailView').style.display = 'flex';

    selectedVehicleId = vehicleId;
    loadVehicleDetails(vehicleId);
    loadVehicleReviews(vehicleId);
}

async function loadCatalog() {
    try {
        const endpoint = userRole === 'ADMIN' ? '/vehicles/admin/all' : '/vehicles';
        const response = await apiFetch(`${DASHBOARD_API_URL}${endpoint}`);
        const vehicles = await response.json();

        currentVehicles = vehicles;
        renderVehicleGrid(vehicles);
        updateStats(vehicles);
    } catch (error) {
        document.getElementById('vehicleGrid').innerHTML = `<p style="color: red; text-align: center;">Failed to load fleet. Backend might be offline.</p>`;
    }
}

async function applyFilters() {
    const type = document.getElementById('filterType').value;
    const status = document.getElementById('filterStatus').value;
    const start = document.getElementById('filterStartDate').value;
    const end = document.getElementById('filterEndDate').value;

    const params = new URLSearchParams();

    if (type) params.append('type', type);
    if (status) params.append('status', status);
    if (start) params.append('startDate', start);
    if (end) params.append('endDate', end);

    const url = `${DASHBOARD_API_URL}/vehicles/filter?${params.toString()}`;

    try {
        const response = await apiFetch(url);

        if (!response.ok) {
            throw new Error(`Filter error: ${response.status}`);
        }

        const vehicles = await response.json();
        renderVehicleGrid(vehicles);
    } catch (error) {
        console.error("Filtering failed:", error);
        const grid = document.getElementById('vehicleGrid');
        grid.innerHTML = `<div style="text-align: center; color: var(--danger); padding: 2rem;">
            Failed to filter fleet. Please try again.
        </div>`;
    }
}

function renderVehicleGrid(vehicles) {
    const grid = document.getElementById('vehicleGrid');
    grid.innerHTML = '';

    if (vehicles.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 3rem;">No vehicles found matching criteria.</div>`;
        return;
    }

    vehicles.forEach(v => {
        const card = document.createElement('div');
        card.className = 'vehicle-card';
        card.onclick = () => showDetailView(v.id);

        let statusColor = v.status === 'AVAILABLE' ? '#22c55e' : (v.status === 'BOOKED' ? '#eab308' : '#ef4444');

        card.innerHTML = `
            <div style="position: absolute; top: 1rem; right: 1rem; background: ${statusColor}; color: white; padding: 0.2rem 0.8rem; border-radius: 12px; font-size: 0.75rem; font-weight: bold;">
                ${v.status}
            </div>
            <img src="${v.imageUrl || 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvcXd5vYpDWGgyZCXrtPg2B0nNbRg523gdYA&s'}" alt="${v.model}">
            <h3 style="margin: 0.5rem 0 0.2rem 0;">${v.make} ${v.model}</h3>
            <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1rem;">${v.vehicleType} • ${v.vehicleTransmission}</p>
            <div style="font-size: 1.25rem; font-weight: bold; color: var(--accent);">₹${v.dailyRate} <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-muted);">/ day</span></div>
        `;
        grid.appendChild(card);
    });
}

function updateStats(vehicles) {
    document.getElementById('statTotal').textContent = vehicles.length;
    document.getElementById('statAvailable').textContent = vehicles.filter(v => v.status === 'AVAILABLE').length;
    document.getElementById('statBooked').textContent = vehicles.filter(v => v.status === 'BOOKED').length;
}

function loadVehicleDetails(id) {
    const vehicle = currentVehicles.find(v => v.id === id);
    if (!vehicle) return;

    document.getElementById('detailTitle').textContent = `${vehicle.make} ${vehicle.model}`;
    document.getElementById('detailImage').src = vehicle.imageUrl || 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvcXd5vYpDWGgyZCXrtPg2B0nNbRg523gdYA&s';
    document.getElementById('detailType').textContent = vehicle.vehicleType;
    document.getElementById('detailTransmission').textContent = vehicle.vehicleTransmission;
    document.getElementById('detailFuel').textContent = vehicle.vehicleFuelType;
    document.getElementById('detailSeats').textContent = vehicle.seatingCapacity;
    document.getElementById('detailPlate').textContent = vehicle.licensePlate;
    document.getElementById('detailPrice').textContent = `₹${vehicle.dailyRate}`;

    const rentBtn = document.getElementById('rentNowBtn');

    rentBtn.onclick = null;

    if (userRole === 'ADMIN') {
        rentBtn.textContent = "Edit Vehicle (Admin)";
        rentBtn.style.background = "#eab308";
        rentBtn.onclick = () => openEditModal(vehicle);

        const existingDeleteBtn = document.getElementById('adminDeleteBtn');
        if (existingDeleteBtn) {
            existingDeleteBtn.remove();
        }

    } else {
        if (vehicle.status !== 'AVAILABLE') {
            rentBtn.textContent = "Currently Unavailable";
            rentBtn.style.background = "var(--text-muted)";
            rentBtn.disabled = true;
        } else {
            rentBtn.textContent = "Book Now";
            rentBtn.style.background = "var(--accent)";
            rentBtn.disabled = false;
            rentBtn.onclick = openBookingModal;
        }
    }
}

function openBookingModal() {
    document.getElementById('bookingModalOverlay').style.display = 'flex';
    document.getElementById('bookingError').classList.remove('active');
    document.getElementById('bookingForm').reset();

    if (!startDatePicker) {
        try {
            startDatePicker = flatpickr("#bookingStartDate", {
                minDate: "today",
                dateFormat: "Y-m-d",
                disableMobile: true,
                onChange: function (selectedDates, dateStr, instance) {
                    if (endDatePicker) {
                        endDatePicker.set('minDate', dateStr);
                    }
                }
            });

            endDatePicker = flatpickr("#bookingEndDate", {
                minDate: "today",
                dateFormat: "Y-m-d",
                disableMobile: true
            });
        } catch (error) {
            console.error("Flatpickr failed to load.", error);
            alert("Warning: Calendar script failed to load. Using standard text inputs.");
        }
    } else {
        startDatePicker.clear();
        endDatePicker.clear();
        endDatePicker.set('minDate', 'today');
    }
}

async function handleBookingSubmit(e) {
    e.preventDefault();
    const errorDiv = document.getElementById('bookingError');
    const submitBtn = e.target.querySelector('button[type="submit"]');

    const payload = {
        vehicleId: selectedVehicleId,
        startDate: document.getElementById('bookingStartDate').value,
        endDate: document.getElementById('bookingEndDate').value
    };

    submitBtn.textContent = "Processing...";
    submitBtn.disabled = true;

    try {
        const response = await apiFetch(`${DASHBOARD_API_URL}/bookings`, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        const data = await response.json();

        if (response.ok) {
            alert("Booking Confirmed!");
            document.getElementById('bookingModalOverlay').style.display = 'none';
            showBookingsView();
        } else {
            showError(errorDiv, data.error || "Failed to book. Dates might overlap.");
        }
    } catch (error) {
        showError(errorDiv, "Connection error.");
    } finally {
        submitBtn.textContent = "Confirm Booking";
        submitBtn.disabled = false;
    }
}

async function loadBookings() {
    const list = document.getElementById('bookingsList');
    list.innerHTML = `<div style="text-align: center; color: var(--text-muted);">Loading bookings...</div>`;
    document.getElementById('bookingsTitle').textContent = userRole === 'ADMIN' ? 'All System Bookings' : 'My Booking History';

    const endpoint = userRole === 'ADMIN' ? '/bookings/admin/all' : '/bookings/my-bookings';

    try {
        const response = await apiFetch(`${DASHBOARD_API_URL}${endpoint}`);
        if (!response.ok) throw new Error(`Server returned ${response.status}`);

        // Save the raw data to our global cache
        currentBookings = await response.json();

        // Trigger the filter logic to render the list
        filterBookings();

    } catch (error) {
        console.error("Booking Fetch Error:", error);
        list.innerHTML = `<div style="color: var(--danger); text-align: center; padding: 2rem;"><strong>Failed to load bookings.</strong></div>`;
    }
}

// Handles frontend filtering and DOM rendering
function filterBookings() {
    const filterValue = document.getElementById('bookingStatusFilter').value;
    const list = document.getElementById('bookingsList');

    // Filter the cached array instantly
    let filtered = currentBookings;
    if (filterValue !== 'ALL') {
        filtered = currentBookings.filter(b => b.status && b.status.toUpperCase() === filterValue);
    }

    if (filtered.length === 0) {
        list.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 2rem;">No bookings found for this status.</div>`;
        return;
    }

    list.innerHTML = ''; 

    filtered.forEach(b => {
        const card = document.createElement('div');
        card.className = 'booking-card';

        const status = b.status ? b.status.toString().toUpperCase() : '';
        let statusColor = status === 'CONFIRMED' ? '#22c55e' : (status === 'CANCELLED' ? '#ef4444' : '#64748b');

        let actionsHtml = '';
        if (status === 'CONFIRMED') {
            actionsHtml += `<button onclick="cancelBooking(${b.id})" class="btn-ghost" style="padding: 0.6rem 1rem; border-color: #ef4444; color: #ef4444; width: 100%;">Cancel</button>`;
            if (userRole === 'ADMIN') {
                actionsHtml += `<button onclick="completeBooking(${b.id})" class="btn-success" style="padding: 0.6rem 1rem; width: 100%; margin-top: 0.5rem;">Mark Completed</button>`;
            }
        } else if (status === 'COMPLETED' && userRole !== 'ADMIN') {
            if (!b.isReviewed) {
                actionsHtml += `<button onclick="openReviewModal(${b.id})" class="btn-primary" style="padding: 0.6rem 1rem; width: 100%;">Leave a Review</button>`;
            } else {
                actionsHtml += `<div style="text-align: center; color: var(--success); font-weight: 600; font-size: 0.9rem; padding: 0.6rem 0; background: rgba(16, 185, 129, 0.1); border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.3);"> Reviewed </div>`;
            }
        }

        const userTag = userRole === 'ADMIN' ? `
            <div class="info-label">Booked by:</div>
            <div class="info-value" style="color: #fbbf24;">${b.userEmail || 'Unknown User'}</div>
        ` : '';

        const vehicleImg = b.vehicleImageUrl || 'https://www.shutterstock.com/image-vector/vector-line-art-car-concept-260nw-2488843165.jpg';

        card.innerHTML = `
            <div class="booking-img-wrapper">
                <img src="${vehicleImg}" alt="${b.vehicleMake} ${b.vehicleModel}" onerror="this.onerror=null; this.src='https://www.shutterstock.com/image-vector/vector-line-art-car-concept-260nw-2488843165.jpg'">
            </div>
            <div class="booking-details">
                <div class="booking-header-row"><h3>${b.vehicleMake} ${b.vehicleModel}</h3></div>
                <div class="info-grid">
                    <div class="info-label">Dates:</div>
                    <div class="info-value">${b.startDate} &rarr; ${b.endDate}</div>
                    ${userTag}
                    <div class="info-label total-row">Total:</div>
                    <div class="info-value total-row" style="font-size: 1.2rem; color: var(--accent);">₹${b.totalAmount}</div>
                </div>
            </div>
            <div class="booking-actions-col">
                <div style="color: ${statusColor}; font-weight: 800; letter-spacing: 1px; font-size: 0.85rem; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${statusColor};"></span>
                    ${status}
                </div>
                ${actionsHtml}
            </div>
        `;
        list.appendChild(card);
    });
}

async function cancelBooking(id) {
    if (!confirm("Are you sure you want to cancel this booking?")) return;
    try {
        const response = await apiFetch(`${DASHBOARD_API_URL}/bookings/${id}/cancel`, { method: 'PUT' });
        if (response.ok) { alert("Booking cancelled."); loadBookings(); }
    } catch (error) { console.error(error); }
}

async function completeBooking(id) {
    try {
        const response = await apiFetch(`${DASHBOARD_API_URL}/bookings/admin/${id}/complete`, { method: 'PUT' });
        if (response.ok) loadBookings();
    } catch (error) { console.error(error); }
}

async function handleAddVehicle(e) {
    e.preventDefault();
    const payload = {
        make: document.getElementById('addMake').value,
        model: document.getElementById('addModel').value,
        dailyRate: document.getElementById('addRate').value,
        vehicleType: document.getElementById('addType').value,
        vehicleTransmission: document.getElementById('addTransmission').value,
        vehicleFuelType: document.getElementById('addFuel').value,
        seatingCapacity: document.getElementById('addSeats').value,
        licensePlate: document.getElementById('addPlate').value,
        imageUrl: document.getElementById('addImage').value || null
    };
    try {
        const response = await apiFetch(`${DASHBOARD_API_URL}/vehicles`, { method: 'POST', body: JSON.stringify(payload) });
        if (response.ok) {
            alert("Vehicle added!");
            document.getElementById('addModalOverlay').style.display = 'none';
            loadCatalog();
        }
    } catch (error) { console.error(error); }
}

function openEditModal(vehicle) {
    document.getElementById('editCarId').value = vehicle.id;
    document.getElementById('editMake').value = vehicle.make;
    document.getElementById('editModel').value = vehicle.model;
    document.getElementById('editRate').value = vehicle.dailyRate;
    document.getElementById('editStatus').value = vehicle.status;
    document.getElementById('editModalOverlay').style.display = 'flex';
}

async function handleEditVehicle(e) {
    e.preventDefault();
    const id = document.getElementById('editCarId').value;
    const existingVehicle = currentVehicles.find(v => v.id == id);
    const payload = {
        make: document.getElementById('editMake').value,
        model: document.getElementById('editModel').value,
        dailyRate: document.getElementById('editRate').value,
        vehicleType: existingVehicle.vehicleType,
        vehicleTransmission: existingVehicle.vehicleTransmission,
        vehicleFuelType: existingVehicle.vehicleFuelType,
        seatingCapacity: existingVehicle.seatingCapacity,
        licensePlate: existingVehicle.licensePlate,
        imageUrl: existingVehicle.imageUrl,
        status: document.getElementById('editStatus').value
    };
    try {
        const response = await apiFetch(`${DASHBOARD_API_URL}/vehicles/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
        if (response.ok) {
            alert("Updated!");
            document.getElementById('editModalOverlay').style.display = 'none';
            showCatalogView();
        }
    } catch (error) { console.error(error); }
}

function openReviewModal(bookingId) {
    document.getElementById('reviewBookingId').value = bookingId;
    document.getElementById('reviewForm').reset();
    const errorDiv = document.getElementById('reviewError');
    if (errorDiv) errorDiv.classList.remove('active');
    document.getElementById('reviewModalOverlay').style.display = 'flex';
}

async function handleReviewSubmit(e) {
    e.preventDefault();
    const errorDiv = document.getElementById('reviewError');
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const payload = {
        bookingId: document.getElementById('reviewBookingId').value,
        rating: parseInt(document.getElementById('reviewRating').value),
        comment: document.getElementById('reviewComment').value.trim()
    };
    submitBtn.textContent = "Submitting...";
    submitBtn.disabled = true;
    try {
        const response = await apiFetch(`${DASHBOARD_API_URL}/reviews`, { method: 'POST', body: JSON.stringify(payload) });
        if (response.ok) {
            alert("Review submitted!");
            document.getElementById('reviewModalOverlay').style.display = 'none';
            loadBookings();
        } else {
            const data = await response.json();
            showError(errorDiv, data.error || "Submission failed.");
        }
    } catch (error) { showError(errorDiv, "Connection error."); }
    finally { submitBtn.textContent = "Submit Review"; submitBtn.disabled = false; }
}

async function loadVehicleReviews(vehicleId) {
    const container = document.getElementById('reviewsContainer');
    container.innerHTML = '<div style="text-align: center; color: var(--text-muted);">Loading reviews...</div>';

    try {
        const response = await apiFetch(`${DASHBOARD_API_URL}/reviews/vehicle/${vehicleId}`);
        if (!response.ok) throw new Error("Failed to fetch reviews");

        const reviews = await response.json();

        if (reviews.length === 0) {
            container.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 2rem; font-style: italic;">No reviews yet. Be the first to rent and rate this vehicle!</div>';
            return;
        }

        container.innerHTML = '';
        reviews.forEach(review => {
            const stars = '⭐'.repeat(review.rating) + '☆'.repeat(5 - review.rating);

            const date = new Date(review.createdAt).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });

            const commentHtml = review.comment
                ? `"${review.comment}"`
                : '<span style="color: var(--text-muted); font-style: italic;">No comment provided.</span>';

            const currentUserEmail = localStorage.getItem('user_email');

            let deleteBtnHtml = '';
            if (userRole === 'ADMIN' || currentUserEmail === review.reviewerEmail) {
                deleteBtnHtml = `<button onclick="deleteReview(${review.id})" class="btn-text-only" style="color: var(--danger); font-size: 0.8rem; margin-left: 1rem;">Delete</button>`;
            }

            const reviewHtml = `
                <div style="background: var(--bg-color); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--border-color); box-shadow: var(--shadow-soft);">
                    <div style="margin-bottom: 0.8rem; letter-spacing: 2px; font-size: 1.1rem;">${stars}</div>
                    <div style="color: var(--text-main); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1rem; font-style: italic;">
                        ${commentHtml}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px dashed var(--border-color); padding-top: 0.8rem;">
                        <div style="display: flex; align-items: center;">
                            <span style="font-weight: 600; color: var(--accent); font-size: 0.9rem;">— ${review.reviewerFirstName || 'User'}</span>
                            ${deleteBtnHtml} 
                        </div>
                        <div style="color: var(--text-muted); font-size: 0.8rem;">${date}</div>
                    </div>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', reviewHtml);
        });

    } catch (error) {
        console.error("Error loading reviews:", error);
        container.innerHTML = '<div style="color: var(--danger); text-align: center;">Failed to load reviews.</div>';
    }
}

// Add this at the end of your dashboard.js file
async function deleteReview(reviewId) {
    if (!confirm("Are you sure you want to delete this review?")) return;

    try {
        const response = await apiFetch(`${DASHBOARD_API_URL}/reviews/${reviewId}`, {
            method: 'DELETE'
        });

        if (response.ok || response.status === 204) {
            alert("Review deleted successfully.");
            // Refresh the reviews list without closing the detail view
            loadVehicleReviews(selectedVehicleId);
            // Also refresh bookings silently so the "Leave a Review" button comes back in the My Bookings tab
            loadBookings();
        } else {
            const data = await response.json();
            alert(data.error || "Failed to delete review.");
        }
    } catch (error) {
        console.error(error);
        alert("Connection error.");
    }
}