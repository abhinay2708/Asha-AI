"""
AI Triage Engine - Uses Gemini, OpenAI, or Anthropic to analyze symptoms.
Returns structured JSON per the specified system prompt.
"""
import json
import re
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from ..config import get_settings
from ..models.schemas import TriageResponse
from .ai_service import analyze_symptoms_gemini


SYSTEM_PROMPT = """You are a rural healthcare assistant. You help triage patients by analyzing their symptoms.
IMPORTANT: You must NEVER provide definitive medical diagnoses. Use guiding language only (e.g., "suspected", "may indicate", "could suggest").
Your role is to help prioritize care and suggest when professional evaluation is needed.
CRITICAL: The values in your JSON response (condition_suspected, severity, advice, specialist_needed) MUST be fully translated into the language specified in the user prompt. 
HOWEVER, the 'severity' field MUST ONLY be one of these exact English strings: "Green", "Yellow", or "Red". Even if you translate other fields, KEEP 'severity' in English!

Analyze the patient's symptoms and return ONLY valid JSON with exactly these keys:
- condition_suspected: A brief description of what might be going on (use cautious language)
- severity: One of "Green" (minor, self-care possible), "Yellow" (moderate, seek care soon), "Red" (urgent, seek care immediately)
- advice: Practical next steps for the patient
- specialist_needed: The type of specialist if any (e.g., "General Physician", "Pediatrician", "None" for Green)

Return ONLY the JSON object, no markdown, no explanation, no extra text."""


class TriageService:
    """Service for AI-powered symptom triage."""
    
    def __init__(self):
        self.settings = get_settings()
        self._openai_client: AsyncOpenAI | None = None
        self._anthropic_client: AsyncAnthropic | None = None
    
    @property
    def openai_client(self) -> AsyncOpenAI:
        """Lazy-load OpenAI client."""
        if self._openai_client is None:
            if not self.settings.openai_api_key:
                raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY in .env")
            self._openai_client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        return self._openai_client
    
    @property
    def anthropic_client(self) -> AsyncAnthropic:
        """Lazy-load Anthropic client."""
        if self._anthropic_client is None:
            if not self.settings.anthropic_api_key:
                raise ValueError("Anthropic API key not configured. Set ANTHROPIC_API_KEY in .env")
            self._anthropic_client = AsyncAnthropic(api_key=self.settings.anthropic_api_key)
        return self._anthropic_client
    
    def _extract_json(self, text: str) -> dict:
        """Extract JSON from AI response, handling markdown code blocks."""
        text = text.strip()
        # Remove markdown code blocks if present
        json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if json_match:
            text = json_match.group(1).strip()
        return json.loads(text)
    
    async def analyze_symptoms(self, symptoms: str, language: str = "en") -> TriageResponse:
        """
        Analyze patient symptoms and return triage result.
        Uses Gemini, OpenAI, or Anthropic based on configuration.
        """
        if self.settings.ai_provider == "gemini" and self.settings.gemini_api_key:
            return await analyze_symptoms_gemini(symptoms, language)
        if self.settings.ai_provider == "anthropic" and self.settings.anthropic_api_key:
            user_message = f"Patient symptoms (language: {language}): {symptoms}"
            return await self._analyze_with_anthropic(user_message)
        user_message = f"Patient symptoms (language: {language}): {symptoms}"
        return await self._analyze_with_openai(user_message)
    
    async def _analyze_with_openai(self, user_message: str) -> TriageResponse:
        """Analyze using OpenAI GPT."""
        response = await self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
        )
        content = response.choices[0].message.content
        data = self._extract_json(content)

        # Translate localized severity to English if needed
        localized_severity = data.get("severity")
        if isinstance(localized_severity, str):
            from .ai_service import SEVERITY_TRANSLATIONS
            # Normalize and translate
            normalized = localized_severity.strip().lower()
            data["severity"] = SEVERITY_TRANSLATIONS.get(normalized, localized_severity)

        return TriageResponse(**data)
    
    async def _analyze_with_anthropic(self, user_message: str) -> TriageResponse:
        """Analyze using Anthropic Claude."""
        response = await self.anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        content = response.content[0].text
        data = self._extract_json(content)

        # Translate localized severity to English if needed
        localized_severity = data.get("severity")
        if isinstance(localized_severity, str):
            from .ai_service import SEVERITY_TRANSLATIONS
            # Normalize and translate
            normalized = localized_severity.strip().lower()
            data["severity"] = SEVERITY_TRANSLATIONS.get(normalized, localized_severity)

        return TriageResponse(**data)
