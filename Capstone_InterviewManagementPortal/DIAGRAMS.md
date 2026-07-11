# Diagrams

## Table of Contents
- [System Architecture Diagram](#system-architecture-diagram)
- [High-Level Component Diagram](#high-level-component-diagram)
- [Logical ER Diagram](#logical-er-diagram)
- [Data Flow Diagram](#data-flow-diagram)
- [Authentication Flow Diagram](#authentication-flow-diagram)
- [Schedule Interview Sequence Diagram](#schedule-interview-sequence-diagram)
- [Submit Feedback Sequence Diagram](#submit-feedback-sequence-diagram)
- [Candidate Lifecycle Diagram](#candidate-lifecycle-diagram)
- [Dashboard Data Flow Diagram](#dashboard-data-flow-diagram)
- [Folder Structure Diagram](#folder-structure-diagram)

## System Architecture Diagram
```mermaid
flowchart TB
    U[End User] --> F[React Frontend]
    F -->|Axios / HTTP Basic| A[FastAPI Backend]
    A --> R[Router Layer]
    R --> S[Service Layer]
    S --> P[Repository Layer]
    P --> M[(MongoDB)]
    A --> D[Swagger / OpenAPI]
```

## High-Level Component Diagram
```mermaid
flowchart LR
    subgraph Frontend
        PAGES[Pages]
        COMPONENTS[Components]
        SERVICES[API Services]
        SESSION[Session Utils]
    end

    subgraph Backend
        ROUTERS[Routers]
        SERVICES_B[Services]
        REPOS[Repositories]
        SCHEMAS[Schemas]
        UTILS[Auth / Validation / Logging]
    end

    PAGES --> COMPONENTS
    PAGES --> SERVICES
    SERVICES --> SESSION
    SERVICES --> ROUTERS
    ROUTERS --> SERVICES_B
    SERVICES_B --> REPOS
    SERVICES_B --> SCHEMAS
    REPOS --> MONGO[(MongoDB)]
```

## Logical ER Diagram
```mermaid
%%{init: {"theme": "base", "er": {"layoutDirection": "LR"}} }%%
erDiagram
    USERS ||--o{ INTERVIEWS : interviewer_id
    USERS ||--o{ CANDIDATE_STATUS_HISTORY : updated_by
    USERS ||--o| CANDIDATE_RESUMES : uploaded_by
    JOBS ||--o{ CANDIDATES : applied_job_id
    JOBS ||--o{ INTERVIEWS : job_id
    CANDIDATES ||--o{ INTERVIEWS : candidate_id
    CANDIDATES ||--o{ CANDIDATE_STATUS_HISTORY : candidate_id
    CANDIDATES ||--|| CANDIDATE_RESUMES : candidate_id

    USERS {
        objectid _id PK
        string name
        string email UK
        string password_base64
        string role
        boolean is_active
        boolean requires_password_reset
    }

    JOBS {
        objectid _id PK
        string jobTitle
        string jobDetails
        string jobRole
        array[string] requiredSkills
        string experienceRequired
        string employmentType
        string location
        datetime created_at
        datetime updated_at
    }

    CANDIDATES {
        objectid _id PK
        string first_name
        string last_name
        string email UK
        string mobile UK
        string current_company
        string total_experience
        objectid applied_job_id FK
        string status
        datetime created_at
        datetime updated_at
    }

    INTERVIEWS {
        objectid _id PK
        objectid candidate_id FK
        objectid job_id FK
        objectid interviewer_id FK
        date interview_date
        string interview_time
        array[string] focus_tech_areas
        string status
        object feedback
        objectid feedback_by FK
        datetime feedback_submitted_at
        datetime created_at
        datetime updated_at
    }

    CANDIDATE_RESUMES {
        objectid _id PK
        objectid candidate_id FK
        string original_filename
        string stored_filename
        string content_type
        binary file_data
        datetime uploaded_at
        objectid uploaded_by FK
    }

    CANDIDATE_STATUS_HISTORY {
        objectid _id PK
        objectid candidate_id FK
        string previous_status
        string new_status
        datetime timestamp
        objectid updated_by FK
    }
```

## Data Flow Diagram
```mermaid
flowchart LR
    U[User] --> L[Login / Browser Session]
    L --> API[Backend API]
    API --> VAL[Validation]
    VAL --> BUS[Business Rules]
    BUS --> DB[(MongoDB)]
    DB --> BUS --> API --> L --> U
```

## Authentication Flow Diagram
```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Repo

    User->>Frontend: Submit login form
    Frontend->>Backend: POST /auth/login
    Backend->>Repo: Find user by email
    Repo-->>Backend: User document
    Backend->>Backend: Compare Base64 password and status
    Backend-->>Frontend: Success response
    Frontend->>Frontend: Store Basic auth token and role
    Frontend->>Backend: Authenticated request
    Backend->>Backend: Enforce role-based dependency
```

## Schedule Interview Sequence Diagram
```mermaid
sequenceDiagram
    participant HR
    participant UI
    participant API
    participant Service
    participant Repo
    participant DB

    HR->>UI: Fill schedule interview form
    UI->>API: POST /api/v1/interviews/
    API->>API: Validate HR role and request body
    API->>Service: create_interview()
    Service->>Repo: Check candidate, job, interviewer, conflicts
    Repo->>DB: Read/write interview record
    DB-->>Repo: Stored interview
    Repo-->>Service: Interview data
    Service-->>API: Response DTO
    API-->>UI: Success envelope
```

## Submit Feedback Sequence Diagram
```mermaid
sequenceDiagram
    participant I as Interviewer
    participant UI as Frontend
    participant API as Backend
    participant S as Feedback Service
    participant R as Interview Repository
    participant DB as MongoDB

    I->>UI: Enter feedback scores and recommendation
    UI->>API: POST /api/v1/interviews/{id}/feedback
    API->>API: Validate interviewer role
    API->>S: submit_feedback()
    S->>R: Update interview feedback
    R->>DB: Persist embedded feedback document
    DB-->>R: Updated document
    R-->>S: Stored feedback
    S-->>API: Feedback response
    API-->>UI: Success envelope
```

## Candidate Lifecycle Diagram
```mermaid
stateDiagram-v2
    [*] --> PROFILE_CREATED
    PROFILE_CREATED --> INTERVIEW_SCHEDULED
    INTERVIEW_SCHEDULED --> INTERVIEW_COMPLETED
    INTERVIEW_COMPLETED --> SELECTED
    INTERVIEW_COMPLETED --> REJECTED
```

## Dashboard Data Flow Diagram
```mermaid
flowchart TB
    HR[HR / Admin / Interviewer] --> DASH[Dashboard Screen]
    DASH --> API[Dashboard Endpoint]
    API --> SVC[Dashboard Service]
    SVC --> REPO[Interview Repository]
    REPO --> JOBS[(jobs)]
    REPO --> CANDS[(candidates)]
    REPO --> INTS[(interviews)]
    JOBS --> REPO
    CANDS --> REPO
    INTS --> REPO
    REPO --> API --> DASH --> HR
```

## Folder Structure Diagram
```mermaid
flowchart TB
    ROOT[Capstone_InterviewManagementPortal]
    ROOT --> BE[backend]
    ROOT --> FE[frontend]
    ROOT --> DOCS[docs]

    BE --> BE_SRC[src]
    BE --> BE_TESTS[tests]
    BE --> BE_POSTMAN[postman]
    BE --> BE_LOGS[logs]

    BE_SRC --> BE_CORE[core]
    BE_SRC --> BE_ROUTERS[routers]
    BE_SRC --> BE_SERVICES[services]
    BE_SRC --> BE_REPOS[repositories]
    BE_SRC --> BE_SCHEMAS[schemas]
    BE_SRC --> BE_UTILS[utils]
    BE_SRC --> BE_CONSTANTS[constants]
    BE_SRC --> BE_ENUMS[enums]

    FE --> FE_SRC[src]
    FE_SRC --> FE_COMPONENTS[components]
    FE_SRC --> FE_PAGES[pages]
    FE_SRC --> FE_SERVICES[services]
    FE_SRC --> FE_UTILS[utils]
    FE_SRC --> FE_CONSTANTS[constants]
    FE_SRC --> FE_STYLES[styles]
