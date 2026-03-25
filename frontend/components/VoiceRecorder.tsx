"use client";

import { useState, useRef, useCallback } from "react";
import { Mic, MicOff, Loader2, AlertCircle } from "lucide-react";
import { analyzeAndSaveScreening, type ScreeningResponse } from "@/lib/api";

type LanguageCode = "en" | "te" | "hi" | "bn" | "mr" | "or";

const LANGUAGES: { code: LanguageCode; label: string }[] = [
  { code: "en", label: "English" },
  { code: "te", label: "తెలుగు" },
  { code: "hi", label: "हिन्दी" },
  { code: "bn", label: "বাংলা" },
  { code: "mr", label: "मराठी" },
  { code: "or", label: "ଓଡ଼ିଆ" },
];

// Browser Speech Recognition types (Chrome, Edge, Safari)
interface SpeechRecognitionEvent extends Event {
  resultIndex: number;
  results: SpeechRecognitionResultList;
}
interface SpeechRecognitionErrorEvent extends Event {
  error: string;
}
declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

interface VoiceRecorderProps {
  patientId?: string;
  onResult?: (screening: ScreeningResponse) => void;
}

export function VoiceRecorder({ patientId = "patient_demo", onResult }: VoiceRecorderProps) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [status, setStatus] = useState<"idle" | "listening" | "processing" | "success" | "error">(
    "idle"
  );
  const [result, setResult] = useState<ScreeningResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [language, setLanguage] = useState<LanguageCode>("en");
  const recognitionRef = useRef<any>(null);

  const getSpeechRecognition = useCallback(() => {
    if (typeof window === "undefined") return null;
    const SpeechRecognitionAPI =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    return SpeechRecognitionAPI ? new SpeechRecognitionAPI() : null;
  }, []);

  const startListening = useCallback(() => {
    const Recognition = getSpeechRecognition();
    if (!Recognition) {
      setError("Speech recognition is not supported in this browser. Try Chrome or Edge.");
      return;
    }

    setError(null);
    setTranscript("");
    setResult(null);
    setStatus("listening");

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = language === "te" ? "te-IN" : language === "hi" ? "hi-IN" : language === "bn" ? "bn-IN" : language === "mr" ? "mr-IN" : language === "or" ? "or-IN" : "en-IN";

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      let final = "";
      let interim = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const r = event.results[i];
        const t = r[0]?.transcript ?? "";
        if (r.isFinal) final += t;
        else interim += t;
      }
      setTranscript((prev) => {
        const base = prev.trim();
        if (final) return base ? `${base} ${final}`.trim() : final.trim();
        return base || interim;
      });
    };

    recognition.onerror = (event: Event) => {
      const err = (event as { error?: string }).error;
      if (err === "no-speech") return;
      setError(`Speech error: ${err ?? "unknown"}`);
      stopListening();
    };

    recognitionRef.current = recognition;
    recognition.start();
    setIsListening(true);
  }, [language, getSpeechRecognition]);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      recognitionRef.current = null;
    }
    setIsListening(false);
  }, []);

  const handleSubmit = useCallback(async () => {
    const text = transcript.trim();
    if (!text) {
      setError("Please speak your symptoms first.");
      return;
    }

    setStatus("processing");
    setError(null);

    try {
      const screening = await analyzeAndSaveScreening(patientId, text, language);
      setResult(screening);
      setStatus("success");
      onResult?.(screening);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed. Please try again.");
      setStatus("error");
    }
  }, [transcript, patientId, language, onResult]);

  const reset = useCallback(() => {
    stopListening();
    setTranscript("");
    setResult(null);
    setError(null);
    setStatus("idle");
  }, [stopListening]);

  const isProcessing = status === "processing";

  return (
    <div className="w-full max-w-lg mx-auto">
      {/* Language selector */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-slate-600 mb-2">
          Select your language
        </label>
        <div className="flex flex-wrap gap-2">
          {LANGUAGES.map(({ code, label }) => (
            <button
              key={code}
              type="button"
              onClick={() => setLanguage(code)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                language === code
                  ? "bg-teal-600 text-white shadow-md"
                  : "bg-white text-slate-600 border border-slate-200 hover:border-teal-400 hover:bg-teal-50"
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Press to Speak button */}
      <div className="flex flex-col items-center gap-6">
        <button
          type="button"
          onClick={isListening ? stopListening : startListening}
          disabled={isProcessing}
          className={`relative flex h-28 w-28 items-center justify-center rounded-full shadow-lg transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-teal-300 disabled:opacity-60 disabled:cursor-not-allowed ${
            isListening
              ? "bg-red-500 hover:bg-red-600 text-white animate-pulse"
              : "bg-teal-500 hover:bg-teal-600 text-white"
          }`}
          aria-label={isListening ? "Stop recording" : "Start recording"}
        >
          {isProcessing ? (
            <Loader2 className="h-12 w-12 animate-spin" />
          ) : isListening ? (
            <MicOff className="h-12 w-12" />
          ) : (
            <Mic className="h-12 w-12" />
          )}
        </button>
        <p className="text-slate-600 text-center text-sm">
          {isListening
            ? "Listening… Describe your symptoms. Tap to stop."
            : isProcessing
              ? "AI is analyzing your symptoms…"
              : "Press to speak your symptoms"}
        </p>
      </div>

      {/* Transcript or Typing */}
      {!result && (
        <div className="mt-6 p-4 bg-white rounded-xl border border-slate-200 shadow-sm">
          <label htmlFor="symptoms-input" className="text-sm font-medium text-slate-500 mb-2 block">
            Describe your symptoms or use the microphone:
          </label>
          <textarea
            id="symptoms-input"
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            placeholder="E.g., I have a headache and mild fever since yesterday..."
            className="w-full min-h-[100px] p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-800 resize-y"
            disabled={isListening || isProcessing}
          />
          <button
            type="button"
            onClick={handleSubmit}
            disabled={isProcessing || !transcript.trim()}
            className="mt-4 w-full py-3 px-4 bg-teal-600 hover:bg-teal-700 disabled:bg-teal-400 text-white font-medium rounded-lg transition-colors"
          >
            {isProcessing ? (
              <span className="flex items-center justify-center gap-2">
                <Loader2 className="h-5 w-5 animate-spin" /> Processing…
              </span>
            ) : (
              "Analyze with AI"
            )}
          </button>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-red-800 text-sm font-medium">Error</p>
            <p className="text-red-700 text-sm">{error}</p>
            <button
              type="button"
              onClick={reset}
              className="mt-2 text-red-600 hover:text-red-800 text-sm font-medium"
            >
              Try again
            </button>
          </div>
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="mt-6 p-6 bg-white rounded-xl border border-slate-200 shadow-md">
          <div className="flex items-center gap-2 mb-4">
            <span
              className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                result.severity === "Red"
                  ? "bg-red-100 text-red-800"
                  : result.severity === "Yellow"
                    ? "bg-amber-100 text-amber-800"
                    : "bg-green-100 text-green-800"
              }`}
            >
              {result.severity} — {result.ai_result.condition_suspected}
            </span>
          </div>
          <p className="text-slate-700 mb-4">{result.ai_result.advice}</p>
          <p className="text-sm text-slate-500">
            Suggested specialist: {result.ai_result.specialist_needed}
          </p>
          <button
            type="button"
            onClick={reset}
            className="mt-6 w-full py-2 text-teal-600 hover:text-teal-800 font-medium text-sm"
          >
            New screening
          </button>
        </div>
      )}
    </div>
  );
}
