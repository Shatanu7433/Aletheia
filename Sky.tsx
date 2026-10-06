const stars = [
  "radial-gradient(1px 1px at 20px 30px,#fff,transparent)",
  "radial-gradient(1px 1px at 140px 80px,#fff,transparent)",
  "radial-gradient(1.5px 1.5px at 90px 150px,#fff,transparent)",
  "radial-gradient(1px 1px at 180px 190px,#fff,transparent)",
].join(",");
const flowers = [
  "radial-gradient(circle at 20% 30%,rgba(140,155,235,.7) 0 5px,transparent 6px)",
  "radial-gradient(circle at 70% 60%,rgba(215,150,205,.6) 0 5px,transparent 6px)",
  "radial-gradient(circle at 45% 85%,rgba(120,140,225,.6) 0 4px,transparent 5px)",
].join(",");

export default function Sky() {
  return (
    <div aria-hidden className="fixed inset-0 -z-10 overflow-hidden bg-night">
      <div className="absolute inset-0" style={{ background: "linear-gradient(180deg,#4a6db3 0%,#6f93d3 20%,#9aa6dc 38%,#cfa9d6 54%,#f1b7b0 66%,#f7d2a6 74%,#7a74ad 84%,#0b0e22 100%)" }} />
      <div className="absolute inset-x-0 top-0 h-3/5 opacity-60" style={{ backgroundImage: stars, backgroundSize: "200px 200px", animation: "twinkle 6s ease-in-out infinite", maskImage: "linear-gradient(#000,transparent)" , WebkitMaskImage: "linear-gradient(#000,transparent)" }} />
      <div className="drift absolute -left-[10%] top-[60%] h-44 w-[65%] rounded-full bg-white/25 blur-3xl" />
      <div className="drift absolute right-[-10%] top-[66%] h-52 w-[70%] rounded-full bg-[#ffd9b8]/30 blur-3xl [animation-delay:-12s]" />
      <div className="absolute inset-x-0 bottom-0 h-[34%]" style={{ backgroundImage: flowers, backgroundSize: "46px 46px", filter: "blur(1.2px)", maskImage: "linear-gradient(transparent,#000 60%)", WebkitMaskImage: "linear-gradient(transparent,#000 60%)" }} />
      <div className="absolute inset-x-0 bottom-0 h-[42%]" style={{ background: "linear-gradient(transparent,rgba(7,9,20,.75) 55%,#070914)" }} />
    </div>
  );
}
