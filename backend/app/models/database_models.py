"""
Database document models and enums.
"""
from enum import Enum
from datetime import datetime
from typing import TypedDict, Optional, Literal


class UserRole(str, Enum):
    """User role enumeration."""
    PATIENT = "Patient"
    DOCTOR = "Doctor"


class Severity(str, Enum):
    """Triage severity levels."""
    GREEN = "Green"
    YELLOW = "Yellow"
    RED = "Red"


class UserDocument(TypedDict, total=False):
    """User document structure in MongoDB."""
    id: str
    name: str
    role: str
    location: str
    created_at: datetime


class ScreeningDocument(TypedDict, total=False):
    """Screening document structure in MongoDB."""
    id: str
    patient_id: str
    transcript: str
    ai_result: dict
    severity: str
    timestamp: datetime


class ClinicDocument(TypedDict, total=False):
    """Clinic document structure in MongoDB."""
    id: str
    name: str
    specialty: str
    distance_km: float
    created_at: datetime
