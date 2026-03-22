# Product Inventory Dashboard

Welcome to the Product Inventory Dashboard! This is a frontend application built to view, search, filter, sort, and manage products dynamically. This project was built entirely from scratch using pure HTML, CSS, and JavaScript, without reliance on external frameworks or libraries.

---

## About This Project

This is a browser-based Product Inventory Dashboard built using pure HTML, CSS,
and JavaScript. No frameworks or external libraries were used at any point.

In this project, I built a fully functional inventory management system where
products are stored as JavaScript objects in an array. The dashboard lets users
view, search, filter, sort, add, edit, and delete products. All data is saved
using localStorage so nothing is lost after a page refresh.

The main goal of this assignment was to practice core frontend concepts like
DOM manipulation, JavaScript array methods, event handling, asynchronous
programming using Promises, and data persistence using localStorage.

---

## How to Run It

### Option 1 — Open Directly in Browser

1. Download or clone the repository
2. Navigate to `mini_app/product_inventory_dashboard/`
3. Double-click `index.html` or right-click → Open with Chrome / Edge / Firefox
4. No installation, server, or build tools are required

The dashboard will load automatically with default product data.

---

## Project Structure

I kept HTML, CSS, and JavaScript in separate files as required by the
assignment. Mixing all code into one file would make it harder to read,
debug, and maintain.

---

## Product Data Used

I used 10 default products spread across 4 categories. I deliberately
included products with different stock levels so I could test every
feature properly.

| # | Product | Category | Price (₹) | Stock | Reason Included |
|---|---------|----------|-----------|-------|-----------------|
| 1 | Wireless Headphones | Electronics | 2999 | 15 | Normal in-stock case |
| 2 | USB-C Charging Cable | Electronics | 399 | 3 | Low stock test (qty < 5) |
| 3 | Mechanical Keyboard | Electronics | 4500 | 0 | Out of stock test |
| 4 | Cotton T-Shirt | Clothing | 599 | 40 | High stock case |
| 5 | Denim Jeans | Clothing | 1299 | 2 | Low stock test (qty < 5) |
| 6 | Running Shoes | Clothing | 3499 | 0 | Out of stock test |
| 7 | Notebook A5 | Stationery | 149 | 80 | Highest stock case |
| 8 | Ballpoint Pen Set | Stationery | 99 | 4 | Low stock test (qty < 5) |
| 9 | Almonds 500g | Food | 549 | 20 | Normal in-stock case |
| 10 | Green Tea 50 Bags | Food | 299 | 0 | Out of stock test |

I added 3 out-of-stock products so the Out of Stock analytics counter
always has something to show. I added 3 low stock products so the low
stock filter is testable from the start without having to add new data.

---

## Features

### Core Features

- Dynamic product card rendering using JavaScript, no hardcoded product
  HTML is present anywhere in `index.html`
- Real-time search by product name (case-insensitive)
- Filter products by category using a dropdown that is populated
  dynamically from the data no hardcoded category options
- Filter products by low stock, shows only products where quantity is
  less than 5
- Sort products by price (low to high, high to low) and by name
  (A to Z, Z to A)
- All search, filter, and sort controls work together simultaneously
- Inventory analytics showing total products, total inventory value
  (price × stock), and out of stock count
- Add new products using a validated form
- Edit existing product details with the form pre-filled
- Delete products with a confirmation dialog
- Data persists using localStorage adding, editing, or deleting
  products is saved across page refreshes
- Simulated async API loading using Promise and setTimeout with a
  loading spinner shown during the delay

### Bonus Features

- All filters, search, and sort work correctly together without breaking
- Category count badges showing how many products exist per category
- Empty state message shown when no products match the current filters
- Fully responsive layout — works on mobile, tablet, and desktop

---

## Functions Used in the Program

| Function | Purpose |
|----------|---------|
| `fetchProductsFromAPI()` | Returns a Promise that resolves after 1.5 seconds with product data, simulating a real API call |
| `renderProducts(productList)` | Builds and injects product cards into the grid dynamically from an array |
| `escapeHTML(str)` | Sanitizes user input before injecting into innerHTML to prevent broken layouts |
| `applyFilters()` | Reads all 4 controls and renders the correctly filtered and sorted product list |
| `updateAnalytics(productList)` | Calculates and updates the 3 stat cards in the analytics section |
| `updateCategoryCounts(productList)` | Counts products per category and renders the pill badges |
| `populateCategoryDropdown()` | Reads unique categories from the data and fills the filter dropdown |
| `validateForm()` | Checks all 4 form fields before submission and shows inline error messages |
| `handleFormSubmit(event)` | Handles both Add and Edit mode depending on whether editingId is set |
| `enterEditMode(productId)` | Pre-fills the form with a product's data and switches the form to edit mode |
| `exitEditMode()` | Resets the form title, button text, and editingId back to add mode |
| `handleDeleteClick(event)` | Handles delete button clicks using event delegation on the grid |
| `handleEditClick(event)` | Handles edit button clicks using event delegation on the grid |
| `saveToLocalStorage()` | Saves the current products array to localStorage as a JSON string |
| `setupEventListeners()` | Wires up all controls and buttons to their handler functions |
| `init()` | Entry point — shows spinner, fetches data, sets up listeners, renders dashboard |

---

## JavaScript Concepts Used

| Concept | How I Used It |
|---------|---------------|
| Arrays | Used for the products list and for filtering and sorting operations |
| Objects | Each product is stored as an object with id, name, category, price, stock |
| `forEach()` | Used to loop through products and build a card for each one |
| `filter()` | Used to apply search, category, and low stock filters |
| `sort()` | Used to sort products by price or name after filtering |
| `reduce()` | Used to calculate total inventory value and category counts |
| `find()` / `findIndex()` | Used to locate a product by ID for edit and delete operations |
| `Promise` + `setTimeout` | Used to simulate an async API call with a network delay |
| `async` / `await` | Used in `init()` to wait for the simulated API before rendering |
| `localStorage` | Used to save and load the products array across page refreshes |
| `JSON.stringify` / `JSON.parse` | Used to convert the array to a string for storage and back |
| Event delegation | Used so one click listener on the grid handles all card buttons |
| Template literals | Used to build product card HTML strings cleanly |
| Spread operator | Used to copy the products array before filtering so the original is not mutated |
| `Set` | Used to extract unique category names from the products array |
| Ternary operator | Used for stock badge logic inside renderProducts |
| `preventDefault()` | Used in form submit handler to stop page refresh |

---

## Key Design Decisions

### Why event delegation for Delete and Edit buttons?

Instead of adding a click listener to every individual button inside
every card, I added a single listener to the product grid container.
When a button is clicked, the event bubbles up to the grid and I check
`event.target.classList` to identify whether it was a delete or edit
button. This is much more efficient, especially when products are added
and removed dynamically, because new cards do not need new listeners.

### Why `applyFilters()` is the central function?

Every single control (search, category, low stock, sort) calls the same
`applyFilters()` function. This function reads all 4 controls at once
and applies them in sequence, filter first, sort last. This design
means all filters always work together correctly. If each control had
its own render logic separately, combining them would have caused bugs.

### Why sort after filtering?

Sorting is always applied on the already-filtered result, not on the
full products array. If sorting happened first, the filtered result
would lose the sort order. Filtering first and sorting last guarantees
the displayed list is always both filtered and sorted correctly.

### Why check localStorage inside the Promise?

The simulated API mimics what a real backend does return whatever
data is available. If the user has saved data in localStorage, that is
returned. If not, the default products are returned. This way
persistence and the loading simulation work naturally together.

---

## Screenshots

### Screenshot 1 — Full Dashboard
![Full Dashboard](screenshots/screenshot1.png)

This screenshot shows the complete dashboard on first load with all 10 default
products rendered. The analytics section shows Total Products as 10, Total
Inventory Value as ₹96,036.00, and Out of Stock count as 3. The category
badges show Electronics 3, Clothing 3, Stationery 2, and Food 2. Each product
card shows the name, category, price, quantity, and a colour-coded stock badge.
Cards with stock 0 show a red Out of Stock badge, cards with stock less than 5
show an orange Low Stock badge, and the rest show a green In Stock badge.

---

### Screenshot 2 — Search Feature Active
![Search Active](screenshots/screenshot2.png)

This screenshot shows the real-time search working. I typed "Cotton" in the
search field and the grid immediately filtered down to just one result —
Cotton T-Shirt. The analytics also updated to reflect the filtered view,
showing Total Products as 1, Total Inventory Value as ₹23,960.00, Out of
Stock as 0, and the category badge showing only Clothing 1. This confirms
that search, analytics, and category counts all update together in real time.

---

### Screenshot 3 — Category Filter and Sort Active Together
![Filters and Sort](screenshots/screenshot3.png)

This screenshot shows multiple controls working simultaneously. I selected
Electronics from the category dropdown and set Sort By to Name A → Z. The
grid shows only the 4 Electronics products sorted alphabetically — Mechanical
Keyboard, Mouse, USB-C Charging Cable, Wireless Headphones. Analytics updated
to show 4 products, ₹62,649.00 total value, and 1 out of stock. This
confirms that filtering and sorting work correctly together.

---

### Screenshot 4 — Add Product Form
![Add Product Form](screenshots/screenshot4.png)

This screenshot shows the Add New Product form filled in with a new product —
Earbuds, priced at ₹2199, stock quantity 66, category Electronics. The form
is at the bottom of the page below the product grid. All 4 fields have labels
and the submit button reads Add Product. After clicking Add Product, the new
card appeared in the grid immediately without any page refresh.

---

## Final Note

This assignment helped me practice how to structure a frontend project
properly with separated HTML, CSS, and JavaScript files. The most
important thing I learned was how to design a central filter function
that all controls plug into because trying to manage search, filter,
and sort as separate independent features leads to conflicts. Having one
function read all the state and produce one result made everything
cleaner and easier to debug.

The async loading simulation also helped me understand how Promises and
await work the dashboard cannot render until the data is ready, which
is exactly how real applications behave when fetching from a server.