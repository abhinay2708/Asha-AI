/**
 * API client for Asha AI backend.
 */

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface TriageResult {
  condition_suspected: string;
  severity: "Green" | "Yellow" | "Red";
  advice: string;
  specialist_needed: string;
}

export interface ScreeningResponse {
  id: string;
  patient_id: string;
  transcript: string;
  ai_result: TriageResult;
  severity: string;
  timestamp: string;
}

export async function analyzeAndSaveScreening(
  patientId: string,
  transcript: string,
  language: string = "en"
): Promise<ScreeningResponse> {
  const res = await fetch(`${API_BASE}/screenings/analyze-and-save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      patient_id: patientId,
      transcript,
      language,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Failed to analyze symptoms");
  }

  return res.json();
}
