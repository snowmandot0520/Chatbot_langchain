import { HeroHighlight } from "../components";
const ErrorPage = () => {
  const focusStyles =
    "focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50";

  return (
    <HeroHighlight>
      <div className="h-screen flex flex-col justify-center items-center mx-auto px-4 py-8 font-mono">
        <h1 className="text-6xl font-bold mb-4 text-white">Error 404</h1>
        <p className="text-xl mb-4">Page Not Found</p>
        <button
          className={`w-3/4 relative inline-flex h-11 overflow-hidden rounded-lg p-[1px] ${focusStyles}`}
          onClick={() => (window.location.href = "/")}
        >
          <span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
          <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-lg bg-slate-950 hover:bg-[#050c2e] transition-all duration-150 ease-in px-3 py-1 text-md font-bold text-white backdrop-blur-3xl">
            Back to Home
          </span>
        </button>
      </div>
    </HeroHighlight>
  );
};

export default ErrorPage;
