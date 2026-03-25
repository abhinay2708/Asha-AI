"""
Clinic service - Fetch clinics (with dummy/seed data support).
"""
from ..database import Database
from ..models.schemas import ClinicResponse


class ClinicService:
    """Service for clinic data."""

    COLLECTION = "clinics"

    @classmethod
    def _get_collection(cls):
        return Database.get_db()[cls.COLLECTION]

    @classmethod
    async def list_all(cls) -> list[ClinicResponse]:
        """List all clinics, sorted by distance."""
        cursor = (
            cls._get_collection()
            .find({})
            .sort("distance_km", 1)
        )
        docs = await cursor.to_list(length=100)
        return [
            ClinicResponse(
                id=str(d["_id"]),
                name=d["name"],
                specialty=d["specialty"],
                distance_km=d["distance_km"],
                created_at=d.get("created_at"),
            )
            for d in docs
        ]
