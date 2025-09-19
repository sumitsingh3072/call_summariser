# Call Summariser - Frontend (Vite)

This frontend is now a small Vite + React app. It uploads a `.txt` transcript to the backend API (`POST /analyze`) and displays the analysis (summary + sentiment).

Prerequisites
- Node >=16 and npm

Install & run (development)

```powershell
cd c:\ML_Projects\call_summariser\frontend
npm install
npm run dev
```

This starts the Vite dev server (hot reload). Open the printed local URL (usually `http://localhost:5173`). By default the app posts to `http://localhost:8000/analyze` unless you override the API base URL with an environment variable.

Using a custom backend URL

Create a `.env` file in the `frontend` folder and set `VITE_API_URL`. Example `.env` contents:

```text
VITE_API_URL=http://localhost:8000
```

Vite exposes variables prefixed with `VITE_` to the client via `import.meta.env`. The app uses `VITE_API_URL` when present; otherwise it falls back to `http://localhost:8000`.

Build & preview

```powershell
npm run build
npm run preview
```

CORS & backend notes
- The backend `backend/app/main.py` already allows `http://localhost` and `http://localhost:3000` in CORS. If you run the dev server on another port, add the origin to the backend's `origins` list.
- Ensure the backend is running and `GROQ_API_KEY` is configured if you want the analysis to work end-to-end.

