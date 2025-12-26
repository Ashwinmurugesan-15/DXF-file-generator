# Production Guide

This application is ready for production.

## Prerequisites
- Python 3.8+
- Node.js 16+

## Quick Start (Production)
Double-click `start_prod.bat`. 
This script will:
1.  Install frontend dependencies.
2.  Build the React frontend into the `backend/static` directory.
3.  Start the FastAPI backend server.
4.  Serve the application at `http://localhost:8000`.

## Manual Setup
If you prefer to run commands manually:

1.  **Build Frontend**:
    ```bash
    cd frontend
    npm install
    npm run build
    ```

2.  **Start Backend**:
    ```bash
    cd ..
    python -m backend.main
    ```

## Configuration
- **Templates**: Edit `frontend/src/templates.json` to add/remove preset options.
- **Logging**: Logs are written to `backend/server.log`.
