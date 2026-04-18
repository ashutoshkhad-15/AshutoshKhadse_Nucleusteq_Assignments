# Todo Management System 

## 1. Project Description
A RESTful API for managing Todo tasks with a focus on clean architecture and strict business rules. Beyond basic CRUD (Create, Read, Update, Delete) operations, this project focuses on **Data Integrity** and **State Management**. It enforces strict business rules regarding how a task moves from one state to another, ensuring that the system remains reliable and predictable.

## 2. Internal Technical Architecture
The project follows a **Layered Architecture** pattern to ensure a clean separation of concerns:

* **Controller Layer:** Acts as the API Gateway. It handles incoming HTTP requests, performs initial DTO validation using `@Valid`, and coordinates the response using `ResponseEntity`.
* **Service Layer:** This is where the business logic resides, such as checking for whitespace-only titles using `.isBlank()` and validating status transitions.
* **Repository Layer:** Utilizes Spring Data JPA to interface with the H2 In-Memory database, abstracting complex SQL queries into simple Java methods.
* **Exception Handling:** A centralized `GlobalExceptionHandler` intercepts errors (like `404 Not Found` or `400 Bad Request`) and converts them into standardized JSON error responses for the client.

## 3. Tech Stack
* **Language:** Java 17
* **Framework:** Spring Boot 3.5.13
* **Database:** H2 (In-Memory)
* **Persistence:** Spring Data JPA / Hibernate

## 4. Business Logic & Edge Case Handling
* **Status Transitions:** Only transitions between `PENDING` and `COMPLETED` are permitted. Any attempt to set an invalid state triggers a custom `InvalidStatusTransitionException`.
* **Defensive Title Updates:** The service layer prevents updating titles to blank strings or whitespace. If a user sends `"   "`, the update is ignored, and the original title is preserved.
* **Existence Checks:** The system uses a "Find-then-Delete" pattern to ensure consistency and prevent internal server errors when deleting non-existent IDs.

## 5. API Documentation & Testing (Postman)

### A. Create TODO
* **Method:** `POST /todos`
* **Logic:** Automatically sets status to `PENDING` and validates that the title is at least 3 characters.
* **Test Result:** Verified `201 Created` for valid input.

### B. Get All TODOs
* **Method:** `GET /todos`
* **Logic:** Returns a `List` of all tasks stored in the database.
* **Test Result:** Verified `200 OK` with a JSON array of tasks.

### C. Get TODO by ID
* **Method:** `GET /todos/{id}`
* **Logic:** Uses **`@PathVariable`** to retrieve a specific resource.
* **Edge Case:** If the ID does not exist, it throws a custom `TodoNotFoundException`.
* **Test Result:** Verified a custom **`404 Not Found`** response for missing IDs.

### D. Update TODO
* **Method:** `PUT /todos/{id}`
* **Logic:** * Enforces `PENDING <-> COMPLETED` status transitions.
    * Uses `.isBlank()` to prevent updating titles to empty whitespace.
* **Test Result:** Verified that sending `"   "` as a title leaves the original data unchanged.

### E. Delete TODO
* **Method:** `DELETE /todos/{id}`
* **Logic:** Uses a "Find-then-Delete" pattern to ensure the task exists before removal.
* **Test Result:** Verified `204 No Content` on success and `404` for non-existent IDs.

## 5. How to Run
1. Clone the repository.
2. Run `./mvnw spring-boot:run` or execute `TodoApplication.java` from your IDE.
3. The server starts on `http://localhost:8080`.

## 6. Database Access
You can monitor the database state at: `http://localhost:8080/h2-console`
* **JDBC URL:** `jdbc:h2:mem:tododb`
* **User:** `sa`
* **Password:** `password`


# Session 5: Enterprise Flow and Testing

This phase focused on transforming the Todo API into a production-ready system by implementing **Observability**, **Dependency Injection for External Services**, and **Comprehensive Test Automation**.

---

## 1. System Observability (SLF4J Logging)
I implemented a strategic logging hierarchy to ensure the system is "observable" without the need for a debugger.

* **Controller Layer:** Logs incoming requests and API milestones (e.g., `Received request to create Todo`).
* **Service Layer:** Uses `INFO` logs for successful business events and `WARN` logs for edge cases, such as failed lookups or invalid status transitions.
* **Custom Pattern:** Configured a professional console pattern in `application.properties` including timestamps, thread IDs, and log levels for easier debugging.

## 2. External Service Simulation
To demonstrate system integration, we introduced the `NotificationServiceClient`:

* **Purpose:** Simulates an external notification system (like Email or SMS).
* **Implementation:** Injected into the `TodoService` via **Constructor Injection**.
* **Trigger Points:** Automatically dispatches a notification whenever a Todo is **Created**, **Updated to COMPLETED**, or **Deleted**.

## 3. Comprehensive Testing & Quality Assurance
Used **JUnit 5**, **Mockito**, and **MockMvc**.

### A. Service Layer (Unit Testing)
* **Isolation:** Used `@Mock` to isolate the business logic from the database and notification clients.
* **Happy Path:** Validated successful CRUD flows and correct DTO mapping.
* **Red Path (Exception Handling):** Explicitly tested that `TodoNotFoundException` and `InvalidStatusTransitionException` are thrown under the correct conditions.
* **Logic Refinement:** Leveraged coverage reports to identify and fix a status validation edge case where identical status updates were bypassing safety checks.

### B. Controller Layer (Integration Testing)
* **MockMvc:** Used to simulate real HTTP calls (`POST`, `GET`, `PUT`, `DELETE`).
* **Verification:** Verified HTTP Status Codes (`201`, `204`, `404`) and validated JSON response structures using `jsonPath`.
* **Spring Boot 3.4 Compatibility:** Implemented the modern `@MockitoBean` for seamless mock injection into the Spring Application Context.

---

## 4. Code Coverage Report
The project exceeded the mandatory 85% requirement, reaching near-total coverage of all core business components.

### Final Coverage Metrics:
| Layer | Line Coverage |
| :--- | :--- |
| **Overall** | **98%** |
| **Controller Layer** | 100% |
| **Service Layer** | 100% |

---

## How to Run Tests
To verify the coverage and run the test suite:

1.  Open your terminal in the project root.
2.  Run the following command:
    ```bash
    mvn clean test
    ```
3.  **To view the visual report in IntelliJ:** Right-click the `src/test/java` folder and select **'Run All Tests with Coverage'**.