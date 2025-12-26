# Walkthrough - DXF Generator Web App

The CLI-based DXF generator has been successfully migrated to a web application.

## How to Run

1.  **Start the Backend**:
    Run the following command in your terminal:
    ```bash
    uvicorn backend.main:app --reload
    ```

2.  **Access the App**:
    Open your browser and navigate to:
    [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Features

-   **Modern Tech Stack**: React + Vite for a robust frontend experience.
-   **Authentication**: Login page with professional "Slate Blue" design.
-   **Batch Generation**: Generate up to 5 DXF files at once with a configurable limit.
-   **Enhanced UI**:
    -   Capsule-style navigation tabs.
    -   Top Navigation Bar with Logout button.
    -   Auto-clearing inputs.
    -   Responsive grid layout for batch inputs.
    -   Professional blue-grey gradient background.

## Technical Details

-   **Backend**: Python FastAPI (with `ezdxf` for generation).
-   **Frontend**: React + Vite.
-   **Communication**: Fetch API.
-   **Configuration**: `frontend/src/config.js` for app constants.
