"""
Clinics API - List nearby clinics.
"""
from fastapi import APIRouter

from ..models.schemas import ClinicResponse
from ..services.clinic_service import ClinicService

router = APIRouter(prefix="/clinics", tags=["Clinics"])


@router.get("", response_model=list[ClinicResponse])
async def list_clinics() -> list[ClinicResponse]:
    """List all clinics, sorted by distance (nearest first)."""
    return await ClinicService.list_all()
