"use client";
import { motion } from "framer-motion";

export const STAGES: [string, string][] = [
  ["understanding", "Understanding question"],
  ["planning", "Creating research plan"],
  ["searching", "Searching the web"],
  ["reading", "Reading sources"],
  ["comparing", "Comparing findings"],
  ["fact_checking", "Fact checking"],
  ["writing", "Generating report"],
];
export type StageState = Record<string, { status: "active" | "done"; detail?: string }>;

export default function ProgressSteps({ state }: { state: StageState }) {
  return (
    <ol className="space-y-3">
      {STAGES.map(([key, label]) => {
        const s = state[key]?.status;
        return (
          <li key={key} className="flex items-start gap-3">
            <span className="mt-1.5 flex h-4 w-4 items-center justify-center">
              {s === "done" ? <span className="text-good">✓</span> :
               s === "active" ? <motion.span className="h-2.5 w-2.5 rounded-full bg-signal"
                  animate={{ opacity: [1, 0.3, 1] }} transition={{ duration: 1.2, repeat: Infinity }} /> :
               <span className="h-2 w-2 rounded-full border border-white/40" />}
            </span>
            <div>
              <div className={s ? "text-text" : "text-white/45"}>{label}</div>
              {s && state[key].detail && <div className="text-sm text-white/70">{state[key].detail}</div>}
            </div>
          </li>
        );
      })}
    </ol>
  );
}
