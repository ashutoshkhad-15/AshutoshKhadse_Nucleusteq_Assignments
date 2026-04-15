# Session 3: Spring Boot User Management API

## Overview
This project is built with Spring Boot. It demonstrates fundamental backend concepts including strict Layered Architecture, Constructor-based Dependency Injection, and custom Exception Handling.

Data is managed using a thread-safe, in-memory `CopyOnWriteArrayList` to ensure safe concurrent operations without requiring an external database setup.

## Technologies Used
* **Java:** 17
* **Framework:** Spring Boot 3.5.13
* **Build Tool:** Maven
* **Architecture:** Controller-Service-Repository Pattern

## Key Features
* **Thread-Safe Storage:** Uses `CopyOnWriteArrayList` and `AtomicLong` for robust in-memory data management.
* **Strict Dependency Injection:** Exclusively uses Constructor Injection (Zero `@Autowired` field injection).
* **Global Exception Handling:** Clean JSON error responses mapping custom and standard exceptions to proper HTTP status codes (`400 Bad Request`, `404 Not Found`, etc.).
* **Dynamic Search:** Strategy-pattern-inspired dynamic filtering without nested `if-else` blocks.

## Technical Architecture
The project follows the **Strict Layered Architecture** pattern:
1. **Controller Layer:** Handles incoming HTTP requests and maps them to service methods.
2. **Service Layer:** Contains core business logic, normalization, and validation.
3. **Repository Layer:** Manages data persistence (In-memory storage with dummy data).
4. **Exception Layer:** Centralized error handling and custom exception definitions.

## API Endpoints

| Method | Endpoint | Description | Query Params / Body |
| :--- | :--- | :--- | :--- |
| **GET** | `/users/search` | Retrieve a list of users. | `?name`, `?age`, `?role` (Optional) |
| **POST** | `/users/submit` | Create a new user. | JSON Body (Name, Age, Role required) |
| **DELETE** | `/{id}` | Delete a user by ID. | `?confirm=true` (Required) |

## Postman Test Cases

You can import these directly into Postman or manually create the requests to test the API.

### 1. Search API (GET)
**Endpoint:** `http://localhost:8080/users/search`
* **Get All Users:**
    * **Method:** `GET`
    * **URL:** `http://localhost:8080/users/search`
* **Filter by Name:**
    * **Method:** `GET`
    * **URL:** `http://localhost:8080/users/search?name=Priya`
* **Filter by Role (Case-insensitive):**
    * **Method:** `GET`
    * **URL:** `http://localhost:8080/users/search?role=ADMIN`
* **Multiple Filters:**
    * **Method:** `GET`
    * **URL:** `http://localhost:8080/users/search?age=30&role=USER`

### 2. Submit API (POST)
**Endpoint:** `http://localhost:8080/users/submit`
* **Success (201 Created):**
    * **Method:** `POST`
    * **Headers:** `Content-Type: application/json`
    * **Body (raw JSON):**
        ```json
        {
            "name": "Ravi",
            "age": 26,
            "role": "DEVELOPER"
        }
        ```
* **Validation Error - Age Required (400 Bad Request):**
    * **Method:** `POST`
    * **Headers:** `Content-Type: application/json`
    * **Body (raw JSON):**
        ```json
        {
            "name": "Ravi",
            "role": "DEVELOPER"
        }
        ```

### 3. Delete API (DELETE)
**Endpoint:** `http://localhost:8080/users/{id}`
* **Success (200 OK):**
    * **Method:** `DELETE`
    * **URL:** `http://localhost:8080/users/5?confirm=true`
* **Missing Confirmation Required Flag (400 Bad Request):**
    * **Method:** `DELETE`
    * **URL:** `http://localhost:8080/users/5`
* **User Not Found (404 Not Found):**
    * **Method:** `DELETE`
    * **URL:** `http://localhost:8080/users/999?confirm=true`
## How to Run
1. Clone the repository.
2. Navigate to project.
3. Run the application from your IDE or via Maven (`mvn spring-boot:run`).
4. The server will start on `http://localhost:8080`.