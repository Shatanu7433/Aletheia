import { Source } from "@/lib/api";

const tone = { high: "text-good", medium: "text-amber-200", low: "text-bad" } as const;

export default function SourceList({ sources }: { sources: Source[] }) {
  return (
    <ul className="space-y-3">
      {sources.map((s) => (
        <li key={s.id} id={`src-${s.id}`} className="scroll-mt-20 panel rounded-2xl p-3">
          <div className="flex items-baseline justify-between gap-3">
            <a href={s.url} target="_blank" rel="noreferrer" className="text-sm font-medium hover:text-signal">
              {s.id}. {s.title}
            </a>
            <span className={`shrink-0 text-xs ${tone[s.credibility.label]}`}>
              {s.credibility.label} · {s.credibility.score}
            </span>
          </div>
          <div className="text-xs text-white/70">{s.domain}</div>
          {s.summary && <p className="mt-2 text-sm text-white/70">{s.summary}</p>}
        </li>
      ))}
    </ul>
  );
}
