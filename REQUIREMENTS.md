# DXF Generator - Project Requirements

## 1. Project Overview
The DXF Generator is a specialized web application designed for structural engineers to generate and parse AutoCAD-compatible DXF files for I-Beams and Columns.

## 2. Functional Requirements

### 2.1 Component Generation
- **Supported Types**: 
  - **I-Beams**: Configurable by Depth (H), Width (B), Web Thickness (tw), and Flange Thickness (tf).
  - **Columns**: Configurable by Width and Height.
- **Generation Modes**:
  - **Single Mode**: Generate and download a single DXF file for one component.
  - **Batch Mode**: 
    - Support adding up to **5 items** in a single batch.
    - Sequential download with a **500ms delay** between files to ensure reliability and bypass browser popup blockers.

### 2.2 DXF Parsing
- **Upload Functionality**: Users can upload an existing DXF file.
- **Parameter Extraction**: 
  - Extract parameters for Beams (from 12-point LWPOLYLINE).
  - Extract parameters for Columns (from 4-point LWPOLYLINE).
- **Auto-Fill**: Automatically populate input fields with parsed parameters.

### 2.3 Template Management
- **Preset Templates**: Access standard configurations from `templates.json` (IPE, HE, SHS, RHS).
- **Custom Templates**: 
  - Save current configurations as custom templates.
  - Custom templates are persisted in `localStorage`.
- **UI Interactions**:
  - "Click to Load" badge for quick selection.
  - Delete custom templates using a trash icon (restricted to custom templates with ID > 1000).

### 2.4 Authentication
- **Login/Signup**: Mock authentication system for access control.
- **Credentials**: Hardcoded support for `user`/`user`.
- **Session Management**: Redirect to login page if unauthenticated; Logout functionality.

## 3. User Interface (UI) & Experience (UX)

### 3.1 Design Language
- **Theme**: Modern "Slate Blue" professional design.
- **Background**: Light blue-grey gradient.
- **Components**: Capsule-style navigation tabs, responsive grid layouts, and clean input forms.

### 3.2 Feedback & Animations
- **Messages**: Auto-hiding success and error messages (5-6 second timeout).
- **Transitions**: Smooth hover effects on cards, buttons, and badges.
- **Input Handling**: Auto-clear inputs upon successful generation; placeholder range hints (e.g., `50-2000`).

## 4. Technical Requirements

### 4.1 Backend (Python/FastAPI)
- **Library**: `ezdxf` for all DXF operations.
- **Performance**: Lockless execution for parallel request processing.
- **File Management**: 
  - Use `tempfile` and UUIDs for unique, collision-free file generation.
  - Automatic deletion of temporary files via `BackgroundTasks` after serving.
- **API**: 
  - `POST /generate`: Validates and generates DXF.
  - `POST /parse-dxf`: Parses uploaded DXF.

### 4.2 Frontend (React/Vite)
- **State Management**: React `useState` and `useEffect` for local state and persistence.
- **Communication**: Fetch API for backend interaction.
- **Proxy**: Vite proxy configured for `/generate` and `/parse-dxf` to backend (Port 8080).

### 4.3 Environment
- **Ports**: 
  - Frontend: `3000`
  - Backend: `8080`
- **CORS**: Middleware enabled on backend for local development.

## 5. Validation Requirements

### 5.1 Input Validation
- **Frontend**: Prevents zero or negative values; displays range hints.
- **Backend**: `Validator` class enforces physical limits:
  - Beam Depth (H): 50 - 2000mm.
  - Flange Width (B): 50 - 1000mm.
  - Thickness (tw, tf): Must be less than H and B, max 100mm.
  - Column dimensions: 10 - 5000mm.

### 5.2 Error Handling
- Catch `ezdxf.DXFError` for invalid file uploads.
- Catch `HTTPException` for validation failures and return user-friendly messages.
- Global 500 error handler with traceback logging for debugging.
