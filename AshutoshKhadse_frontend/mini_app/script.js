// Will add js code later
console.log("script.js loaded successfully");

// This is the default dataset that will be loaded if no data is found in localStorage.
// nothing is saved in localStorage yet, so this will be the initial data when you first open the app.

const defaultProducts = [
  { id: 1,  name: "Wireless Headphones",  category: "Electronics", price: 2999, stock: 15 },
  { id: 2,  name: "USB-C Charging Cable", category: "Electronics", price: 399,  stock: 3  },
  { id: 3,  name: "Mechanical Keyboard",  category: "Electronics", price: 4500, stock: 0  },
  { id: 4,  name: "Cotton T-Shirt",       category: "Clothing",    price: 599,  stock: 40 },
  { id: 5,  name: "Denim Jeans",          category: "Clothing",    price: 1299, stock: 2  },
  { id: 6,  name: "Running Shoes",        category: "Clothing",    price: 3499, stock: 0  },
  { id: 7,  name: "Notebook A5",          category: "Stationery",  price: 149,  stock: 80 },
  { id: 8,  name: "Ballpoint Pen Set",    category: "Stationery",  price: 99,   stock: 4  },
  { id: 9,  name: "Almonds 500g",         category: "Food",        price: 549,  stock: 20 },
  { id: 10, name: "Green Tea 50 Bags",    category: "Food",        price: 299,  stock: 0  },
];

// This is the live array the app works with. It gets populated on page load either from localStorage or from defaultProducts above. All add / edit / delete operations modify this.
let products = [];

// Tracks the next available unique ID. Set properly during init() so new products never accidentally reuse an existing ID.

let nextId = 1;

// null  = form is in "Add" mode
// number = form is in "Edit" mode, value is the ID of the product being edited

let editingId = null;
