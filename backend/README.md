# Asha AI — Backend (FastAPI)

Rural Healthcare Screening System — API and AI Triage Engine.

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your MongoDB URL and AI API key.

## Seed Data

```bash
python -m scripts.seed_data
```

Inserts 10 clinics, 5 sample screenings, and 4 users.

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

Docs: http://localhost:8000/docs
