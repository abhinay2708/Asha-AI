"""
Triage API - Voice-to-AI symptom analysis endpoint.
"""
from fastapi import APIRouter, HTTPException

from ..models.schemas import TriageRequest, TriageResponse
from ..services.triage_service import TriageService

router = APIRouter(prefix="/triage", tags=["Triage"])
triage_service = TriageService()


@router.post("/analyze", response_model=TriageResponse)
async def analyze_symptoms(request: TriageRequest) -> TriageResponse:
    """
    Analyze patient symptoms via AI.
    Accepts symptom text (from voice transcript) and returns triage result.
    """
    try:
        result = await triage_service.analyze_symptoms(
            symptoms=request.symptoms,
            language=request.language,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage analysis failed: {str(e)}")
