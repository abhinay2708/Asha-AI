"""
Screenings API - CRUD and listing for doctor dashboard.
Analyze-and-save: Gemini triage + persist to MongoDB.
"""
from fastapi import APIRouter, Query, HTTPException

from ..models.schemas import (
    ScreeningCreate,
    ScreeningResponse,
    ScreeningListResponse,
    ScreeningAnalyzeRequest,
)
from ..services.screening_service import ScreeningService
from ..services.triage_service import TriageService

router = APIRouter(prefix="/screenings", tags=["Screenings"])
triage_service = TriageService()


@router.post("/analyze-and-save", response_model=ScreeningResponse, status_code=201)
async def analyze_and_save_screening(data: ScreeningAnalyzeRequest) -> ScreeningResponse:
    """
    Run Gemini triage on symptoms, save to MongoDB, return screening.
    Use this after voice capture: transcript -> AI analysis -> persisted record.
    """
    try:
        triage_result = await triage_service.analyze_symptoms(
            symptoms=data.transcript,
            language=data.language,
        )
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage failed: {str(e)}")

    ai_result = triage_result.model_dump()
    screening_data = ScreeningCreate(
        patient_id=data.patient_id,
        transcript=data.transcript,
        ai_result=ai_result,
    )
    return await ScreeningService.create(screening_data)


@router.post("", response_model=ScreeningResponse, status_code=201)
async def create_screening(data: ScreeningCreate) -> ScreeningResponse:
    """Create a new screening record (called after AI triage)."""
    return await ScreeningService.create(data)


@router.get("/stats")
async def get_severity_stats() -> dict:
    """Get counts by severity for heatmap/stats (Doctor dashboard)."""
    return await ScreeningService.get_severity_counts()


@router.get("", response_model=ScreeningListResponse)
async def list_screenings(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("severity", description="Sort field: severity | timestamp"),
    severity: str | None = Query(None, description="Filter by severity: Red | Yellow | Green"),
) -> ScreeningListResponse:
    """
    List recent screenings. Red severity shown first when sort_by=severity.
    Protected by role - Doctor only (auth middleware to be added).
    """
    screenings, total = await ScreeningService.list_recent(
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        severity_filter=severity,
    )
    return ScreeningListResponse(
        screenings=screenings,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{screening_id}", response_model=ScreeningResponse)
async def get_screening(screening_id: str) -> ScreeningResponse:
    """Get a single screening by ID."""
    screening = await ScreeningService.get_by_id(screening_id)
    if not screening:
        raise HTTPException(status_code=404, detail="Screening not found")
    return screening
