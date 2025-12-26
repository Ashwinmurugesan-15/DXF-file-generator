# Implementation Plan - Migration to Full React (Vite)

The user has requested a standard React frontend. We will migrate from the current "Embedded React" (HTML + Babel blocks) to a full **Vite + React** project structure.

## Proposed Changes

### Structure
- Create `frontend/` directory.
- Initialize with `npx create-vite@latest`.

### Frontend Development
#### [NEW] [frontend/](file:///c:/Users/ashwi/Downloads/dxf_generator/frontend/)
- **Setup**: Install dependencies (`axios` for API calls, maybe `tailwindcss` if desired, though we will stick to CSS modules or standard CSS to match current style).
- **Porting Logic**:
    - Move `App` component from `index.html` to `frontend/src/App.jsx`.
    - Move styles from `index.html` to `frontend/src/App.css` or `index.css`.
    - Factor out components if needed (e.g., `BeamForm`, `BatchControls`).
- **API Integration**:
    - Configure `vite.config.js` to proxy `/generate` -> `http://localhost:8000`.

### Backend
- No changes required to `main.py` logic.
- We might eventually serve the *built* frontend files from FastAPI, but for development:
    - Run Backend on `:8000`.
    - Run Frontend on `:5173`.

## Verification Plan

### Manual Verification
1. `cd frontend` -> `npm install` -> `npm run dev`.
2. Open `localhost:5173`.
3. Verify the UI looks identical to the previous version.
4. Test "Batch Mode" and "Single Mode" generation.
5. Verify downloads work correctly through the proxy.
