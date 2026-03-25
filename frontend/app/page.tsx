import { Heart, Shield } from "lucide-react";
import { VoiceRecorder } from "@/components/VoiceRecorder";

export default function PatientHomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-teal-50/30">
      {/* Header */}
      <header className="border-b border-slate-200/80 bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-600 text-white">
            <Heart className="h-6 w-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-800">Asha AI</h1>
            <p className="text-xs text-slate-500">Rural Healthcare Screening</p>
          </div>
        </div>
      </header>

      {/* Hero */}
      <main className="max-w-2xl mx-auto px-4 py-8 sm:py-12">
        <section className="text-center mb-10">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-800 mb-2">
            Describe your symptoms in your language
          </h2>
          <p className="text-slate-600 text-base sm:text-lg max-w-lg mx-auto">
            Press the microphone, speak clearly, and our AI will help you understand
            next steps. Available in Telugu, Hindi, Bengali, Marathi, Odia & English.
          </p>
        </section>

        {/* Voice recorder card */}
        <section className="bg-white rounded-2xl shadow-lg shadow-slate-200/60 border border-slate-100 p-6 sm:p-8">
          <VoiceRecorder patientId="patient_demo" />
        </section>

        {/* Trust badge */}
        <section className="mt-8 flex items-center justify-center gap-2 text-slate-500 text-sm">
          <Shield className="h-4 w-4 text-teal-600" />
          <span>
            This is a screening aid, not a diagnosis. Always consult a doctor for medical advice.
          </span>
        </section>
      </main>

      {/* Footer */}
      <footer className="mt-auto py-6 text-center text-slate-400 text-sm">
        Asha AI — HackFest 2026
      </footer>
    </div>
  );
}
