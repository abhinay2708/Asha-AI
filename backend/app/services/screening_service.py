"""
Screening service - CRUD operations for screenings in MongoDB.
"""
from datetime import datetime
from bson import ObjectId
from typing import Optional

from ..database import Database
from ..models.schemas import ScreeningResponse, ScreeningCreate


def _serialize_doc(doc: dict) -> dict:
    """Convert MongoDB document to API-friendly format."""
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id", doc.get("id", "")))
    if "timestamp" in doc and isinstance(doc["timestamp"], datetime):
        doc["timestamp"] = doc["timestamp"].isoformat()
    if "created_at" in doc and isinstance(doc["created_at"], datetime):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc


class ScreeningService:
    """Service for screening records."""
    
    COLLECTION = "screenings"
    
    @classmethod
    def _get_collection(cls):
        return Database.get_db()[cls.COLLECTION]
    
    @classmethod
    async def create(cls, data: ScreeningCreate) -> ScreeningResponse:
        """Create a new screening record."""
        severity = data.ai_result.get("severity", "Green")
        doc = {
            "patient_id": data.patient_id,
            "transcript": data.transcript,
            "ai_result": data.ai_result,
            "severity": severity,
            "timestamp": datetime.utcnow(),
            "created_at": datetime.utcnow(),
        }
        result = await cls._get_collection().insert_one(doc)
        doc["_id"] = result.inserted_id
        return ScreeningResponse(
            id=str(result.inserted_id),
            patient_id=doc["patient_id"],
            transcript=doc["transcript"],
            ai_result=doc["ai_result"],
            severity=doc["severity"],
            timestamp=doc["timestamp"],
        )
    
    @classmethod
    async def get_by_id(cls, screening_id: str) -> ScreeningResponse | None:
        """Get a screening by ID."""
        try:
            oid = ObjectId(screening_id)
        except Exception:
            return None
        doc = await cls._get_collection().find_one({"_id": oid})
        if not doc:
            return None
        return ScreeningResponse(
            id=str(doc["_id"]),
            patient_id=doc["patient_id"],
            transcript=doc["transcript"],
            ai_result=doc["ai_result"],
            severity=doc["severity"],
            timestamp=doc["timestamp"],
            created_at=doc.get("created_at"),
        )
    
    @classmethod
    async def list_recent(
        cls,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "severity",
        severity_filter: Optional[str] = None,
    ) -> tuple[list[ScreeningResponse], int]:
        """
        List screenings with optional severity filter.
        Sort order: Red first, then Yellow, then Green when sort_by=severity.
        """
        collection = cls._get_collection()
        match = {}
        if severity_filter:
            match["severity"] = severity_filter

        total = await collection.count_documents(match)

        severity_order = {"Red": 1, "Yellow": 2, "Green": 3}

        if sort_by == "severity":
            cursor = collection.find(match)
            all_docs = await cursor.to_list(length=1000)  # Reasonable limit for demo
            all_docs.sort(
                key=lambda d: (
                    severity_order.get(d.get("severity", ""), 4),
                    -(d.get("timestamp") or datetime.min).timestamp(),
                )
            )
            docs = all_docs[(page - 1) * page_size : page * page_size]
        else:
            sort_direction = -1 if sort_by == "timestamp" else 1
            cursor = (
                collection.find(match)
                .sort(sort_by, sort_direction)
                .skip((page - 1) * page_size)
                .limit(page_size)
            )
            docs = await cursor.to_list(length=page_size)

        screenings = [
            ScreeningResponse(
                id=str(d["_id"]),
                patient_id=d["patient_id"],
                transcript=d["transcript"],
                ai_result=d["ai_result"],
                severity=d["severity"],
                timestamp=d["timestamp"],
                created_at=d.get("created_at"),
            )
            for d in docs
        ]
        return screenings, total
    
    @classmethod
    async def get_severity_counts(cls) -> dict[str, int]:
        """Get count of screenings by severity (for heatmap/stats)."""
        pipeline = [
            {"$group": {"_id": "$severity", "count": {"$sum": 1}}},
            {"$project": {"severity": "$_id", "count": 1, "_id": 0}},
        ]
        collection = cls._get_collection()
        results = await collection.aggregate(pipeline).to_list(None)
        counts = {"Red": 0, "Yellow": 0, "Green": 0}
        for r in results:
            sev = r.get("severity", "Green")
            if sev in counts:
                counts[sev] = r["count"]
        return counts
