"""
Pydantic schemas for API request/response validation.
"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal


# --- User Schemas ---
class UserCreate(BaseModel):
    """Schema for creating a user."""
    name: str = Field(..., min_length=1, max_length=200)
    role: Literal["Patient", "Doctor"] = "Patient"
    location: str = Field(default="", max_length=500)


class UserResponse(BaseModel):
    """Schema for user response."""
    id: str
    name: str
    role: str
    location: str
    created_at: datetime | None = None


# --- Screening Schemas ---
class ScreeningCreate(BaseModel):
    """Schema for creating a screening record."""
    patient_id: str
    transcript: str = Field(..., min_length=1)
    ai_result: dict


class ScreeningResponse(BaseModel):
    """Schema for screening response."""
    id: str
    patient_id: str
    transcript: str
    ai_result: dict
    severity: str
    timestamp: datetime
    created_at: datetime | None = None


class ScreeningListResponse(BaseModel):
    """Schema for paginated screening list."""
    screenings: list[ScreeningResponse]
    total: int
    page: int
    page_size: int


# --- Triage Schemas ---
class TriageRequest(BaseModel):
    """Schema for AI triage request."""
    symptoms: str = Field(..., min_length=1, description="Patient symptom description")
    language: str = Field(default="en", description="Language of the input")


class ScreeningAnalyzeRequest(BaseModel):
    """Schema for analyze-and-save: Gemini triage + save to MongoDB."""
    patient_id: str = Field(..., description="Patient identifier")
    transcript: str = Field(..., min_length=1, description="Voice transcript / symptoms")
    language: str = Field(default="en", description="Language of the input")


class TriageResponse(BaseModel):
    """Schema for AI triage response - matches system prompt output."""
    condition_suspected: str
    severity: Literal["Green", "Yellow", "Red"]
    advice: str
    specialist_needed: str


# --- Clinic Schemas ---
class ClinicResponse(BaseModel):
    """Schema for clinic response."""
    id: str
    name: str
    specialty: str
    distance_km: float
    created_at: datetime | None = None
