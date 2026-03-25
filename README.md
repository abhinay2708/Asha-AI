# Asha AI — Rural Healthcare Screening System

**Asha AI** is a HackFest 2026 winning entry: a voice-powered triage system that helps rural patients describe symptoms in their native language (Telugu, Hindi, Bengali, Marathi, Odia, or English). The system uses AI to suggest likely conditions, severity (Green/Yellow/Red), and next steps—without making definitive diagnoses. Doctors get a dashboard to view screenings sorted by urgency.

---

## Tech Stack

| Layer    | Technology                                      |
| -------- | ----------------------------------------------- |
| Frontend | Next.js 14+ (App Router), Tailwind CSS, Lucide React |
| Backend  | FastAPI (Python)                                |
| Database | MongoDB Atlas                                   |
| Auth     | NextAuth.js / Firebase (Role-Based: Patient, Doctor) |
| Deploy   | Vercel (Frontend) + Railway/Render (Backend)    |

---

## Project Structure

```
Hackfest/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI app, CORS, lifespan
│   │   ├── config.py       # Settings (env vars)
│   │   ├── database.py     # MongoDB connection
│   │   ├── models/         # Pydantic schemas, DB types
│   │   ├── routers/        # API routes (triage, screenings, clinics)
│   │   └── services/       # Triage AI, screening, clinic logic
│   ├── scripts/
│   │   └── seed_data.py    # Dummy data: 10 clinics, 5 screenings
│   ├── requirements.txt
│   ├── .env.example
│   ├── Procfile           # Railway/Render
│   └── railway.json
├── frontend/               # Next.js (to be added)
└── README.md
```

---

## Quick Start (Backend)

### 1. Prerequisites

- Python 3.11+
- MongoDB (local or Atlas)
- OpenAI API key (or Anthropic)

### 2. Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
cp .env.example .env
# Edit .env: set MONGODB_URL, OPENAI_API_KEY
```

### 3. Seed Dummy Data

```bash
python -m scripts.seed_data
```

### 4. Run Server

```bash
uvicorn app.main:app --reload --port 8000
# Or: python run.py
```

API docs: **http://localhost:8000/docs**

---

## API Endpoints

| Method | Endpoint             | Description                    |
| ------ | -------------------- | ------------------------------ |
| POST   | `/triage/analyze`    | AI symptom analysis            |
| POST   | `/screenings`        | Create screening record        |
| GET    | `/screenings`        | List screenings (sortable)     |
| GET    | `/screenings/stats`  | Red/Yellow/Green counts        |
| GET    | `/clinics`           | List nearby clinics            |
| GET    | `/health`            | Health check                   |

---

## Deployment

### Backend (Railway / Render)

1. **Railway**
   - New project → Deploy from GitHub (backend folder or monorepo)
   - Add env vars: `MONGODB_URL`, `OPENAI_API_KEY`
   - Uses `railway.json` for start command and health check

2. **Render**
   - New Web Service → Connect repo
   - Root directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add env vars as above

### Frontend (Vercel)

- Connect GitHub repo, set root to `frontend`
- Add env: `NEXT_PUBLIC_API_URL=https://your-backend.railway.app`
- Deploy

---

## Database Schema

- **users**: `{ id, name, role, location }`
- **screenings**: `{ id, patientId, transcript, ai_result, severity, timestamp }`
- **clinics**: `{ id, name, specialty, distance_km }`

---

## License

MIT — Built for HackFest 2026.
