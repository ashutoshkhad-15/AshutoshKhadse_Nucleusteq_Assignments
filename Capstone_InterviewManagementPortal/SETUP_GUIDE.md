# Setup Guide

## Table of Contents
- [Prerequisites](#prerequisites)
- [Python Installation](#python-installation)
- [Node.js Installation](#nodejs-installation)
- [MongoDB Setup](#mongodb-setup)
- [Environment Configuration](#environment-configuration)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Run the Application](#run-the-application)
- [Common Issues and Fixes](#common-issues-and-fixes)
- [Testing](#testing)
- [Production Deployment Notes](#production-deployment-notes)

## Prerequisites
- Python 3.10+
- Node.js 18+ recommended
- MongoDB 6+ or compatible Atlas instance
- Git

## Python Installation
1. Install Python from the official Python website.
2. Verify installation:
```bash
python --version
```

## Node.js Installation
1. Install Node.js LTS.
2. Verify installation:
```bash
node --version
npm --version
```

## MongoDB Setup
1. Start a local MongoDB server or create a MongoDB Atlas cluster.
2. Create a database for the portal.
3. Confirm the connection URI in `backend/.env`.

## Environment Configuration
### Backend `.env`
```env
PROJECT_NAME=Interview Management Portal
API_V1_STR=/api/v1
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=interview_management_db
ENVIRONMENT=development
LOG_LEVEL=INFO
DEFAULT_ADMIN_PASSWORD=Admin@123
DEFAULT_USER_PASSWORD=Welcome@123
```

### Frontend `.env`
```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Backend Setup
1. Open a terminal in `backend`.
2. Create and activate a virtual environment.
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Start the API:
```bash
python -m uvicorn src.main:app --reload--port 8000
```

## Frontend Setup
1. Open a terminal in `frontend`.
2. Install dependencies:
```bash
npm install
```
3. Start the dev server:
```bash
npm run dev
```

## Run the Application
1. Start MongoDB.
2. Start the backend on port `8000`.
3. Start the frontend on port `5173`.
4. Open the frontend in the browser.

## Common Issues and Fixes
- Backend import errors caused by package version mismatch:
  - Reinstall backend dependencies inside a clean virtual environment.
  - Make sure the `motor` and `pymongo` versions match the pinned requirements.
- CORS errors:
  - Ensure the frontend runs on `http://localhost:5173` or `http://127.0.0.1:5173`.
- Login failure on seeded accounts:
  - Verify the password reset requirement on first login.
- MongoDB connection failure:
  - Confirm the URI, server status, and database name.
- File upload issues:
  - Resume uploads use `multipart/form-data`.

## Testing
Run backend tests from the `backend` directory:
```bash
python -m pytest
```

Coverage output is generated under `backend/htmlcov/` when coverage is enabled.

## Production Deployment Notes
- Set `ENVIRONMENT=production`.
- Use a managed MongoDB service or hardened replica set.
- Replace Basic auth with a stronger authentication mechanism if deploying publicly.
- Run the backend behind a reverse proxy such as Nginx.
- Disable debug-only conveniences and lock down CORS origins.
- Store secrets in environment variables or a secret manager.
