"use client";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

// Turn "[3]" or "[1, 4]" into links to the source cards.
function linkCitations(md: string) {
  const [body, refs] = md.split(/\n## References/);
  const linked = body.replace(/\[(\d+(?:\s*,\s*\d+)*)\]/g, (_, ids: string) =>
    ids.split(",").map((n) => `[${n.trim()}](#src-${n.trim()} "cite")`).join(""));
  return linked + (refs ? "\n## References" + refs : "");
}

export default function ReportView({ markdown }: { markdown: string }) {
  return (
    <article className="report">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ href, title, children }) =>
            title === "cite" ? <a href={href} className="cite">{children}</a>
              : <a href={href} target="_blank" rel="noreferrer">{children}</a>,
        }}
      >
        {linkCitations(markdown)}
      </ReactMarkdown>
    </article>
  );
}
