export const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Source = {
  id: number; url: string; title: string; domain: string; summary: string;
  key_points: string[]; credibility: { score: number; label: "high" | "medium" | "low" };
};
export type Check = { claim: string; status: "supported" | "contested" | "unverified"; source_ids: number[]; note: string };
export type Research = {
  id: string; question: string; status: "running" | "done" | "error"; created_at: number;
  report?: string; sources?: Source[]; checks?: Check[]; error?: string;
};

export async function startResearch(question: string, depth = "standard"): Promise<string> {
  const r = await fetch(`${API}/research`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, depth }),
  });
  if (!r.ok) throw new Error((await r.json()).detail ?? "Could not start research");
  return (await r.json()).id;
}
export const listResearch = async (): Promise<Research[]> =>
  (await fetch(`${API}/research`, { cache: "no-store" })).json();
export const getResearch = async (id: string): Promise<Research> =>
  (await fetch(`${API}/research/${id}`, { cache: "no-store" })).json();
