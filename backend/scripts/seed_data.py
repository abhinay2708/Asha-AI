"""
Seed script - Populate MongoDB with dummy data for demo.
Run: python -m scripts.seed_data (from backend/)
"""
import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "asha_ai")

# 10 local clinics
CLINICS = [
    {"name": "Village Health Centre - Guntur", "specialty": "General", "distance_km": 2.5},
    {"name": "Rural Primary Health Centre", "specialty": "General", "distance_km": 4.0},
    {"name": "Community Clinic - Krishna District", "specialty": "General", "distance_km": 5.2},
    {"name": "Telugu Rural Hospital", "specialty": "Multi-specialty", "distance_km": 8.0},
    {"name": "District Hospital - Vijayawada", "specialty": "Multi-specialty", "distance_km": 12.0},
    {"name": "Maternal & Child Health Centre", "specialty": "Pediatrics", "distance_km": 3.0},
    {"name": "Ayush Dispensary", "specialty": "Alternative Medicine", "distance_km": 6.5},
    {"name": "Sub-Centre - Narsaraopet", "specialty": "General", "distance_km": 7.2},
    {"name": "Mobile Health Unit - Route A", "specialty": "General", "distance_km": 1.5},
    {"name": "Private Clinic - Dr. Rao", "specialty": "General Physician", "distance_km": 9.0},
]

# 5 recent screenings (dummy data)
def make_screenings():
    base_time = datetime.utcnow()
    return [
        {
            "patient_id": "patient_001",
            "transcript": "నాకు జ్వరం మరియు తలనొప్పి ఉంది. రెండు రోజుల నుండి.",
            "ai_result": {
                "condition_suspected": "Possible viral fever or mild infection",
                "severity": "Yellow",
                "advice": "Rest, stay hydrated. Monitor temperature. Seek care if fever persists >3 days.",
                "specialist_needed": "General Physician",
            },
            "severity": "Yellow",
            "timestamp": base_time - timedelta(hours=2),
        },
        {
            "patient_id": "patient_002",
            "transcript": "Mere bachche ko tez bukhaar hai aur pet mein dard hai.",
            "ai_result": {
                "condition_suspected": "Possible gastrointestinal infection or fever in child",
                "severity": "Red",
                "advice": "Seek immediate medical attention. Keep child hydrated.",
                "specialist_needed": "Pediatrician",
            },
            "severity": "Red",
            "timestamp": base_time - timedelta(hours=1),
        },
        {
            "patient_id": "patient_003",
            "transcript": "I have a mild cough and cold for 3 days.",
            "ai_result": {
                "condition_suspected": "Possible mild upper respiratory tract infection",
                "severity": "Green",
                "advice": "Rest, warm fluids, over-the-counter cold medication. See doctor if worsens.",
                "specialist_needed": "None",
            },
            "severity": "Green",
            "timestamp": base_time - timedelta(hours=5),
        },
        {
            "patient_id": "patient_004",
            "transcript": "আমার বুকে ব্যাথা এবং শ্বাসকষ্ট হচ্ছে.",
            "ai_result": {
                "condition_suspected": "Possible respiratory or cardiac concern - requires evaluation",
                "severity": "Red",
                "advice": "Seek immediate medical attention. Do not ignore chest pain and breathlessness.",
                "specialist_needed": "General Physician or Cardiologist",
            },
            "severity": "Red",
            "timestamp": base_time - timedelta(minutes=30),
        },
        {
            "patient_id": "patient_005",
            "transcript": "माझे पोट दुखत आहे, पण जास्त गंभीर नाही.",
            "ai_result": {
                "condition_suspected": "Possible mild indigestion or gastric discomfort",
                "severity": "Green",
                "advice": "Light diet, avoid spicy food. See doctor if pain persists or worsens.",
                "specialist_needed": "None",
            },
            "severity": "Green",
            "timestamp": base_time - timedelta(hours=8),
        },
    ]


async def seed():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]

    # Users
    users_coll = db["users"]
    users = [
        {"name": "Ramesh Kumar", "role": "Patient", "location": "Guntur, Andhra Pradesh"},
        {"name": "Dr. Priya Sharma", "role": "Doctor", "location": "Village Health Centre"},
        {"name": "Lakshmi Devi", "role": "Patient", "location": "Krishna District"},
        {"name": "Dr. Venkat Rao", "role": "Doctor", "location": "District Hospital"},
    ]
    await users_coll.delete_many({})
    await users_coll.insert_many(users)
    print(f"✓ Inserted {len(users)} users")

    # Clinics
    clinics_coll = db["clinics"]
    clinic_docs = [
        {**c, "created_at": datetime.utcnow()} for c in CLINICS
    ]
    await clinics_coll.delete_many({})
    result = await clinics_coll.insert_many(clinic_docs)
    print(f"✓ Inserted {len(result.inserted_ids)} clinics")

    # Screenings
    screenings_coll = db["screenings"]
    screening_docs = [
        {**s, "created_at": datetime.utcnow()} for s in make_screenings()
    ]
    await screenings_coll.delete_many({})
    result = await screenings_coll.insert_many(screening_docs)
    print(f"✓ Inserted {len(result.inserted_ids)} screenings")

    print("\nSeed complete. Database ready for demo.")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
