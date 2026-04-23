const API_VEHICLE_URL = 'http://localhost:8080/api/vehicles';
let currentFleetData = []; 

document.addEventListener('DOMContentLoaded', () => {
    // Auth Guard
    const token = localStorage.getItem('token');
    if (!token) { window.location.href = 'index.html'; return; }

    // Set UI User Details
    const userName = localStorage.getItem('user_name') || 'Member';
    const userRole = localStorage.getItem('user_role') || 'USER';
    
    document.getElementById('welcomeMessage').textContent = userName;
    document.getElementById('roleBadge').textContent = userRole;

    // Load Fleet
    fetchVehicles();
});

// API FETCH & RENDER
async function fetchVehicles(type = '', status = '') {
    const grid = document.getElementById('vehicleGrid');
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center;">Loading premium fleet...</div>';

    try {
        let url = API_VEHICLE_URL;
        if (type || status) {
            url += `/filter?type=${type}&status=${status}`;
        }

        const res = await fetch(url);
        if (!res.ok) throw new Error('API Error');
        
        currentFleetData = await res.json();
        
        updateStats(currentFleetData);
        renderGrid(currentFleetData);
    } catch (err) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; color: #ef4444;">Server connection failed.</div>';
    }
}

function updateStats(vehicles) {
    document.getElementById('statTotal').textContent = vehicles.length;
    document.getElementById('statAvailable').textContent = vehicles.filter(v => v.status === 'AVAILABLE').length;
    document.getElementById('statBooked').textContent = vehicles.filter(v => v.status !== 'AVAILABLE').length;
}

function renderGrid(vehicles) {
    const grid = document.getElementById('vehicleGrid');
    grid.innerHTML = '';

    if (vehicles.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center;">No vehicles match your filter.</div>';
        return;
    }

    // Check if the current logged-in user is an ADMIN
    const isAdmin = localStorage.getItem('user_role') === 'ADMIN';

    vehicles.forEach(v => {
        const imgUrl = v.imageUrl || '';
        const price = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(v.dailyRate);
        const statusColor = v.status === 'AVAILABLE' ? '#22c55e' : '#ef4444';

        // ADMIN EDIT BUTTON LOGIC
        let adminEditHtml = '';
        if (isAdmin) {
            adminEditHtml = `
                <button class="btn-ghost" 
                        style="position:absolute; top: 1rem; right: 1rem; padding: 0.3rem 0.8rem; font-size: 0.75rem; z-index: 10; border-color: var(--accent);" 
                        onclick="event.stopPropagation(); editCar(${v.id})">
                    Edit
                </button>`;
        }

        const card = `
            <div class="vehicle-card" onclick="openDetails(${v.id})">
                <span style="position:absolute; top: 1rem; left: 1rem; font-size:0.75rem; color:${statusColor}; font-weight:700; z-index: 5;">● ${v.status}</span>
                
                ${adminEditHtml} <img src="${imgUrl}" onerror="this.src=''">
                <h3 style="margin-bottom: 0.5rem;">${v.make} ${v.model}</h3>
                <p style="color: var(--accent); font-weight: 700; margin: 0;">${price} <span style="font-size:0.8rem; font-weight:400; color:var(--text-muted)">/day</span></p>
                <button class="btn-ghost" style="width:100%; margin-top: 1.5rem; padding: 0.5rem;">View Details</button>
            </div>
        `;
        grid.insertAdjacentHTML('beforeend', card);
    });
}

function editCar(carId) {
    const car = currentFleetData.find(v => v.id === carId);
    if (!car) return;

    // Fill the form with the car's current data
    document.getElementById('editCarId').value = car.id;
    document.getElementById('editMake').value = car.make;
    document.getElementById('editModel').value = car.model;
    document.getElementById('editRate').value = car.dailyRate;
    document.getElementById('editStatus').value = car.status;

    // Show the overlay (using flex to keep it centered)
    document.getElementById('editModalOverlay').style.display = 'flex';
}

// VIEW SWITCHING LOGIC (SPA) 
function openDetails(carId) {
    const car = currentFleetData.find(v => v.id === carId);
    if (!car) return;

    // 1. POPULATE DETAILS
    document.getElementById('detailTitle').textContent = `${car.make} ${car.model}`;
    
    // We keep a default fallback image just in case the DB image is missing
    const imgUrl = car.imageUrl || '';
    document.getElementById('detailImage').src = imgUrl;
    
    document.getElementById('detailType').textContent = car.vehicleType;
    document.getElementById('detailTransmission').textContent = car.vehicleTransmission;
    document.getElementById('detailFuel').textContent = car.vehicleFuelType;
    document.getElementById('detailSeats').textContent = car.seatingCapacity;
    document.getElementById('detailPlate').textContent = car.licensePlate;
    
    const price = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(car.dailyRate);
    document.getElementById('detailPrice').textContent = price;

    const rentBtn = document.getElementById('rentNowBtn');
    if(car.status === 'AVAILABLE') {
        rentBtn.textContent = 'Book Now';
        rentBtn.disabled = false;
        rentBtn.style.opacity = '1';
    } else {
        rentBtn.textContent = 'Currently Unavailable';
        rentBtn.disabled = true;
        rentBtn.style.opacity = '0.5';
    }

    // THE DYNAMIC BACKGROUND MAGIC
    const hero = document.querySelector('.fullscreen-hero');
    hero.style.backgroundImage = `linear-gradient(rgba(10, 10, 10, 0.85), rgba(10, 10, 10, 0.95)), url('${imgUrl}')`;
    hero.style.backgroundSize = 'cover';
    hero.style.backgroundPosition = 'center';

    // SWAP VIEWS
    document.getElementById('catalogView').style.display = 'none';
    document.getElementById('navCatalogBtn').style.display = 'inline-block';
    document.getElementById('detailView').style.display = 'block';
}

document.getElementById('backToCatalogBtn').addEventListener('click', showCatalog);
document.getElementById('navCatalogBtn').addEventListener('click', showCatalog);

function showCatalog() {
    document.querySelector('.fullscreen-hero').style.backgroundImage = '';

    document.getElementById('detailView').style.display = 'none';
    document.getElementById('navCatalogBtn').style.display = 'none';
    document.getElementById('catalogView').style.display = 'block';
}

// EVENT LISTENERS 
document.getElementById('applyFiltersBtn').addEventListener('click', () => {
    const type = document.getElementById('filterType').value;
    const status = document.getElementById('filterStatus').value;
    fetchVehicles(type, status);
});

document.getElementById('clearFiltersBtn').addEventListener('click', () => {
    document.getElementById('filterType').value = '';
    document.getElementById('filterStatus').value = '';
    fetchVehicles();
});

document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.clear();
    window.location.href = 'index.html';
});

function closeEditModal() {
    document.getElementById('editModalOverlay').style.display = 'none';
}

document.getElementById('closeModalBtn').addEventListener('click', closeEditModal);
document.getElementById('cancelEditBtn').addEventListener('click', closeEditModal);
document.getElementById('editModalOverlay').addEventListener('click', (e) => {
    if (e.target.id === 'editModalOverlay') closeEditModal();
});

document.getElementById('editVehicleForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const carId = parseInt(document.getElementById('editCarId').value);
    const updatedData = {
        make: document.getElementById('editMake').value,
        model: document.getElementById('editModel').value,
        dailyRate: parseFloat(document.getElementById('editRate').value),
        status: document.getElementById('editStatus').value
    };

    // try {
    //     const token = localStorage.getItem('token'); // Use whatever key you settled on
    //     await fetch(`${API_VEHICLE_URL}/${carId}`, {
    //         method: 'PUT',
    //         headers: { 
    //             'Content-Type': 'application/json',
    //             'Authorization': `Bearer ${token}` 
    //         },
    //         body: JSON.stringify(updatedData)
    //     });
    // } catch (error) {
    //     console.error("Database update failed", error);
    // }

    const carIndex = currentFleetData.findIndex(v => v.id === carId);
    if (carIndex > -1) {
        // Merge the new data into the old data
        currentFleetData[carIndex] = { ...currentFleetData[carIndex], ...updatedData };
        
        renderGrid(currentFleetData);  // Redraw the cars with the new price/status
        updateStats(currentFleetData); // Update the Total/Available/Booked numbers at the top
    }

    closeEditModal();
});