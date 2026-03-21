
// This is the default dataset that will be loaded if no data is found in localStorage.
// nothing is saved in localStorage yet, so this will be the initial data when you first open the app.

const defaultProducts = [
    { id: 1, name: "Wireless Headphones", category: "Electronics", price: 2999, stock: 15 },
    { id: 2, name: "USB-C Charging Cable", category: "Electronics", price: 399, stock: 3 },
    { id: 3, name: "Mechanical Keyboard", category: "Electronics", price: 4500, stock: 0 },
    { id: 4, name: "Cotton T-Shirt", category: "Clothing", price: 599, stock: 40 },
    { id: 5, name: "Denim Jeans", category: "Clothing", price: 1299, stock: 2 },
    { id: 6, name: "Running Shoes", category: "Clothing", price: 3499, stock: 0 },
    { id: 7, name: "Notebook A5", category: "Stationery", price: 149, stock: 80 },
    { id: 8, name: "Ballpoint Pen Set", category: "Stationery", price: 99, stock: 4 },
    { id: 9, name: "Almonds 500g", category: "Food", price: 549, stock: 20 },
    { id: 10, name: "Green Tea 50 Bags", category: "Food", price: 299, stock: 0 },
];

// This is the live array the app works with. It gets populated on page load either from localStorage or from defaultProducts above. All add / edit / delete operations modify this.
let products = [];

// Tracks the next available unique ID. Set properly during init() so new products never accidentally reuse an existing ID.

let nextId = 1;

// null  = form is in "Add" mode
// number = form is in "Edit" mode, value is the ID of the product being edited

let editingId = null;

// In a real app this would be a fetch() call to a backend server. Here we simulate that using Promise + setTimeout to mimic the delay of a real network request.
// The function returns a Promise that resolves after 1.5 seconds with the product data.

function fetchProductsFromAPI() {
    return new Promise((resolve) => {

        // Wait 1.5 seconds to simulate network delay
        setTimeout(() => {

            // Checking if the user has previously saved data in localStorage
            const saved = localStorage.getItem("inventoryProducts");

            if (saved) {
                // Return the saved products if they exist
                resolve(JSON.parse(saved));
            } else {
                // Otherwise return the default product list
                resolve(defaultProducts);
            }

        }, 1500); // Here, 1500 milliseconds = 1.5 seconds

    });
}

// This function prevents broken layouts like if someone types characters like < > & in a product name

function escapeHTML(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

// Builds product cards dynamically from the given array. AS No hardcoded product HTML allowed.
// Will get Called every time the list needs to update.

function renderProducts(productList) {
    const grid = document.getElementById("product-grid");

    // Clears existing cards before re-rendering
    grid.innerHTML = "";

    // Show empty state if no products match
    if (productList.length === 0) {
        grid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <p>No products found</p>
        <span>Try adjusting your search or filters, or add a new product below.</span>
      </div>
    `;
        return;
    }

    // Builds a card for each product
    productList.forEach(product => {
        const card = document.createElement("div");
        card.className = "product-card";
        card.dataset.id = product.id;

        // Determines stock badge and card colour strip
        let stockBadgeHTML = "";

        if (product.stock === 0) {
            card.classList.add("out-of-stock");
            stockBadgeHTML = `<span class="stock-badge out-stock">Out of Stock</span>`;
        } else if (product.stock < 5) {
            card.classList.add("low-stock");
            stockBadgeHTML = `<span class="stock-badge low-stock">Low Stock</span>`;
        } else {
            stockBadgeHTML = `<span class="stock-badge in-stock">In Stock</span>`;
        }

        // Injects product data into the card
        card.innerHTML = `
      <p class="product-card-name">${escapeHTML(product.name)}</p>
      <p class="product-card-category">${escapeHTML(product.category)}</p>
      <p class="product-card-price">₹${product.price.toLocaleString("en-IN")}</p>
      <p class="product-card-stock">Qty: ${product.stock}</p>
      ${stockBadgeHTML}
      <div class="card-actions">
        <button class="btn btn-edit" data-id="${product.id}">✏️ Edit</button>
        <button class="btn btn-danger btn-delete" data-id="${product.id}">🗑️ Delete</button>
      </div>
    `;

        grid.appendChild(card);
    });
}

// This function calculates and displays the 3 stat cards: total products, total inventory value, and out of stock count and it will update every time the product list is edited.

function updateAnalytics(productList) {
    // Total number of products in the current list
    const total = productList.length;

    const totalValue = productList.reduce((sum, p) => sum + (p.price * p.stock), 0);

    // Count products where stock has hit zero
    const outOfStock = productList.filter(p => p.stock === 0).length;

    // Push the calculated values into the DOM
    document.getElementById("val-total-products").textContent = total;
    document.getElementById("val-total-value").textContent = "₹" + totalValue.toLocaleString("en-IN", { minimumFractionDigits: 2 });
    document.getElementById("val-out-of-stock").textContent = outOfStock;

    // From Bonus: also update the category count badges
    updateCategoryCounts(productList);
}

// This function is from the bonus category it Counts how many products exist in each category and renders them 

function updateCategoryCounts(productList) {
    const container = document.getElementById("category-counts");

    // Builds an object like { Electronics: 3, Clothing: 2 }
    const counts = productList.reduce((acc, p) => {
        acc[p.category] = (acc[p.category] || 0) + 1;
        return acc;
    }, {});

    // Clears old badges and render fresh ones
    container.innerHTML = "";

    Object.entries(counts).forEach(([category, count]) => {
        const badge = document.createElement("span");
        badge.className = "category-badge";
        badge.innerHTML = `${category} <span class="badge-count">${count}</span>`;
        container.appendChild(badge);
    });
}

// This function reads unique categories from the products array and fills the filter dropdown.
// Get Called on init and after every add/delete in case a new category was introduced.

function populateCategoryDropdown() {
    const select = document.getElementById("category-filter");

    // Gets unique categories and sort alphabetically
    const categories = [...new Set(products.map(p => p.category))].sort();

    // Remembers what the user had selected before rebuilding
    const currentValue = select.value;

    // Resets to just the default option then rebuild
    select.innerHTML = `<option value="all">All Categories</option>`;

    categories.forEach(cat => {
        const option = document.createElement("option");
        option.value = cat;
        option.textContent = cat;
        select.appendChild(option);
    });

    // Restores the previous selection if it still exists
    if (currentValue && categories.includes(currentValue)) {
        select.value = currentValue;
    }
}

// APPLY FILTER is the Central function that reads all 4 controls (search, category, low stock, sort) and renders the correct filtered + sorted list.

function applyFilters() {
    const searchTerm = document.getElementById("search-input").value.trim().toLowerCase();
    const selectedCat = document.getElementById("category-filter").value;
    const lowStockOnly = document.getElementById("low-stock-filter").checked;
    const sortOption = document.getElementById("sort-select").value;

    // Starts with the full products array
    let result = [...products];

    // Filter 1 is Search by name which is case-insensitive
    if (searchTerm) {
        result = result.filter(p => p.name.toLowerCase().includes(searchTerm));
    }

    // Filter 2 is Category dropdown
    if (selectedCat !== "all") {
        result = result.filter(p => p.category === selectedCat);
    }

    // Filter 3 is Low stock only for stock less than 5
    if (lowStockOnly) {
        result = result.filter(p => p.stock < 5);
    }

    // Sort AFTER filtering
    if (sortOption === "price-low") {
        result.sort((a, b) => a.price - b.price);
    } else if (sortOption === "price-high") {
        result.sort((a, b) => b.price - a.price);
    } else if (sortOption === "name-az") {
        result.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortOption === "name-za") {
        result.sort((a, b) => b.name.localeCompare(a.name));
    }

    renderProducts(result);
    updateAnalytics(result);
}

// This function wires up all 4 controls to applyFilters() so the list updates on every interaction

function setupEventListeners() {

    document.getElementById("search-input").addEventListener("input", applyFilters);

    document.getElementById("category-filter").addEventListener("change", applyFilters);

    document.getElementById("low-stock-filter").addEventListener("change", applyFilters);

    document.getElementById("sort-select").addEventListener("change", applyFilters);
}

// This is the first function that runs when the page loads. It shows the loading spinner, waits for the simulated API call to finish, then kicks off the rest of the dashboard.

async function init() {
    // Grab the loading spinner and product grid from the DOM
    const loadingEl = document.getElementById("loading-state");
    const gridEl = document.getElementById("product-grid");

    // Shows the spinner, hide the grid while loading
    loadingEl.classList.remove("hidden");
    gridEl.classList.add("hidden");

    // Wait for the simulated API to return data
    // The "await" pauses here until the Promise resolves
    const fetchedProducts = await fetchProductsFromAPI();

    // Stores the fetched data in our working array
    products = fetchedProducts;

    // Set nextId so new products don't clash with existing IDs
    nextId = Math.max(...products.map(p => p.id)) + 1;

    // Hide the spinner, show the grid
    loadingEl.classList.add("hidden");
    gridEl.classList.remove("hidden");

    populateCategoryDropdown();
    setupEventListeners();
    // Render all products
    applyFilters();
}

// Kick everything off when the page loads
init();
