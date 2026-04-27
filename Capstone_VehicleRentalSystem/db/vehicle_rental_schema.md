# Vehicle Rental System – Database Design Documentation

## 1. Introduction
This document describes the database design and structure of the Vehicle Rental System. The schema is engineered to ensure data integrity, support scalability, and maintain clean integration with Spring Boot (JPA).

---

## 2. ERD (Entity Relationship Diagram)
The diagram below visually represents the tables, relationships, and foreign key constraints.

![Vehicle Rental ER Diagram](./Capstone_VehicleRentalSystem/db/erd/erd.png)

> **Note:** The source file and raw SQL schema are maintained in the `/db/erd/erd.png` directory.

---

## 3. Design Philosophy
The database follows a normalized relational design (3NF) incorporating:
* **Strong Constraints:** Explicit PK, FK, UNIQUE, and CHECK constraints.
* **Auditability:** Standardized `created_at` and `updated_at` fields.
* **State Management:** Status-based logic for soft deletions.
* **Concurrency:** Optimistic locking via a `version` field.

---

## 4. Table Structures

### User Management (`app_users`)
Stores all user-related data including authentication and identity.
* **Uniqueness:** Email, phone, and license are unique to prevent duplicate accounts.
* **RBAC:** Supports `USER` and `ADMIN` roles.
* **Control:** `is_active` enables account suspension without data loss.

### Vehicle Management (`vehicles`)
Represents the rental fleet and its current state.
* **Status Lifecycle:** `AVAILABLE` → `BOOKED` → `MAINTENANCE` → `RETIRED`.
* **Soft Delete:** Vehicles are marked as `RETIRED` rather than being deleted to preserve booking history.
* **Lightweight:** `image_url` is used instead of binary BLOBs for better performance.

### Booking System (`bookings`)
The core transactional table handling reservations.
* **Audit Snapshots:** Stores `price_per_day` at the time of booking to ensure historical accuracy even if rates change.
* **Integrity:** Enforces `end_date > start_date`.
* **Flow:** `PENDING` → `CONFIRMED` → `COMPLETED`.

### Review System (`reviews`)
Stores post-booking feedback.
* **Integrity:** One review per booking (`UNIQUE` constraint).
* **Validation:** Ratings are restricted to a `1–5` range.

---

## 5. Entity Relationships

| Relationship | Type | Logic |
| :--- | :--- | :--- |
| **User → Booking** | One-to-Many | A user can have multiple historical bookings. |
| **Vehicle → Booking** | One-to-Many | A vehicle can be involved in many separate bookings. |
| **Booking → Review** | One-to-One | Each booking transaction allows for exactly one review. |

---

## 6. Key Architectural Decisions

* **Soft Delete Strategy:** Vehicles are never physically deleted. This prevents foreign key orphans and allows for historical revenue reporting.
* **Optimistic Locking:** Uses a `version` column to prevent the "Lost Update" problem during concurrent web requests.
* **Auditing:** Managed via JPA auditing (`@CreatedDate`, `@LastModifiedDate`) to track the data lifecycle automatically.
* **Conflict Handling:** Overlapping booking dates are validated at the **Service Layer** for maximum flexibility and user-friendly error messages.

---

## 7. Indexing Strategy

| Index Name | Purpose |
| :--- | :--- |
| `idx_app_users_email` | Accelerates user lookup during login. |
| `idx_vehicles_search` | Improves performance for fleet filtering (Make/Model). |
| `idx_bookings_dates` | Optimizes availability checks for specific date ranges. |

---

## 8. Conclusion
This design balances capstone simplicity with production-level thinking, ensuring a robust backbone for the Vehicle Rental System that is both scalable and easy to maintain.

---