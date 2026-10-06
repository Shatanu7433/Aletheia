"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { API, getResearch, Research } from "@/lib/api";
import ProgressSteps, { StageState } from "@/components/ProgressSteps";
import ReportView from "@/components/ReportView";
import SourceList from "@/components/SourceList";

export default function ResearchPage() {
  const { id } = useParams<{ id: string }>();
  const [state, setState] = useState<StageState>({});
  const [data, setData] = useState<Research | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let es: EventSource | null = null;
    getResearch(id).then((r) => {
      setData(r);
      if (r.status !== "running") return;
      es = new EventSource(`${API}/research/${id}/stream`);
      es.onmessage = async (m) => {
        const ev = JSON.parse(m.data);
        if (ev.stage === "complete") { es?.close(); setData(await getResearch(id)); }
        else if (ev.stage === "error") { es?.close(); setError(ev.detail || "Research failed"); }
        else setState((s) => ({ ...s, [ev.stage]: { status: ev.status, detail: ev.detail } }));
      };
      es.onerror = () => es?.close();
    });
    return () => es?.close();
  }, [id]);

  if (!data) return <p className="px-6 pt-40 text-center text-white/75">Loading…</p>;
  const failed = error || data.status === "error";

  return (
    <div className="mx-auto max-w-6xl px-6 pb-24 pt-32">
      <h1 className="max-w-3xl font-serif text-4xl leading-[1.05] tracking-tight md:text-5xl">{data.question}</h1>

      {failed ? (
        <p className="panel mt-10 rounded-3xl p-6 text-bad">{error || data.error || "Research failed."} Check your API keys and try again.</p>
      ) : data.status === "running" ? (
        <div className="panel mt-10 max-w-xl rounded-3xl p-7">
          <h2 className="mb-5 font-serif text-2xl">Researching…</h2>
          <ProgressSteps state={state} />
        </div>
      ) : (
        <div className="mt-10 grid gap-8 lg:grid-cols-[minmax(0,1fr)_330px]">
          <div className="panel rounded-3xl p-8 md:p-10">
            <div className="mb-6 flex gap-2">
              <a href={`${API}/research/${id}/download`} className="glass rounded-full px-5 py-2 text-sm transition hover:bg-white hover:text-night">Download .md</a>
              <button onClick={() => window.print()} className="glass rounded-full px-5 py-2 text-sm transition hover:bg-white hover:text-night">Print / PDF</button>
            </div>
            <ReportView markdown={data.report ?? ""} />
          </div>
          <aside>
            <h2 className="mb-3 font-serif text-2xl">{data.sources?.length ?? 0} sources</h2>
            <SourceList sources={data.sources ?? []} />
          </aside>
        </div>
      )}
    </div>
  );
}
