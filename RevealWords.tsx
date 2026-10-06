export default function RevealWords({ lines, className = "" }: { lines: string[]; className?: string }) {
  let i = 0;
  return (
    <h1 className={className}>
      {lines.map((line, li) => (
        <span key={li} className="block">
          {line.split(" ").map((w, wi) => (
            <span key={wi}>
              {wi > 0 && " "}
              <span className="word-wrapper">
                <span className="word-inner" style={{ animationDelay: `${i++ * 0.09}s` }}>{w}</span>
              </span>
            </span>
          ))}
        </span>
      ))}
    </h1>
  );
}
