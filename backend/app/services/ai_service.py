"""
AI Service - Google Gemini integration for symptom triage.
"""
import asyncio
import json
import re

from ..config import get_settings
from ..models.schemas import TriageResponse

SYSTEM_PROMPT = """You are a rural healthcare assistant. You help triage patients by analyzing their symptoms.
IMPORTANT: You must NEVER provide definitive medical diagnoses. Use guiding language only (e.g., "suspected", "may indicate", "could suggest").
Your role is to help prioritize care and suggest when professional evaluation is needed.
CRITICAL: The values in your JSON response (condition_suspected, severity, advice, specialist_needed) MUST be fully translated into the language specified in the user prompt. The JSON keys themselves MUST remain in English!

Analyze the patient's symptoms and return ONLY valid JSON with exactly these keys:
- condition_suspected: A brief description of what might be going on (use cautious language)
- severity: One of "Green" (minor, self-care possible), "Yellow" (moderate, seek care soon), "Red" (urgent, seek care immediately)
- advice: Practical next steps for the patient
- specialist_needed: The type of specialist if any (e.g., "General Physician", "Pediatrician", "None" for Green)

Return ONLY the JSON object, no markdown, no explanation, no extra text."""


def _extract_json(text: str) -> dict:
    """Extract JSON from AI response, handling markdown code blocks."""
    text = text.strip()
    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if json_match:
        text = json_match.group(1).strip()
    return json.loads(text)


def _analyze_with_gemini_sync(user_message: str) -> TriageResponse:
    """Synchronous Gemini call (runs in thread pool for async)."""
    import google.generativeai as genai

    settings = get_settings()
    if not settings.gemini_api_key:
        raise ValueError(
            "Gemini API key not configured. Set GEMINI_API_KEY in .env"
        )

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(
        model_name=settings.gemini_model or "gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
        generation_config=genai.types.GenerationConfig(temperature=0.3),
    )

    response = model.generate_content(user_message)

    content = response.text if response.text else str(response)
    data = _extract_json(content)
    return TriageResponse(**data)


async def analyze_symptoms_gemini(symptoms: str, language: str = "en") -> TriageResponse:
    """
    Analyze patient symptoms using Google Gemini.
    Runs in thread pool to avoid blocking the event loop.
    """
    user_message = f"Patient symptoms (language: {language}): {symptoms}"
    return await asyncio.to_thread(_analyze_with_gemini_sync, user_message)
