import { HeroHighlight } from "../components";

const HomePage = () => {
  const focusStyles =
    "focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50";

  return (
    <HeroHighlight>
      <div className="h-screen flex flex-col justify-center mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-4">Welcome to Revlis Chat</h1>
        <h3 className="text-xl font-[500] mb-4">
          Your Personalized Medical Assistant
        </h3>
        <p className="text-lg mb-4 w-3/4">
          Welcome to our state-of-the-art chatbot, powered by cutting-edge
          technology to provide you with accurate and helpful medical
          information. Our chatbot is built using the LLaMA-2 model fine-tuned
          with a vast collection of medical papers, ensuring you get precise and
          relevant answers to your health-related questions.
        </p>
        {/* <button className="z-0 w-1/6 bg-blue-500 hover:bg-blue-700 py-2 px-4 rounded transition-all duration-150 ease-in">
          <span className="inline-block text-white text-center font-bold">
            Start Chat
          </span>
        </button> */}
        <button
          onClick={() => (window.location.href = "/chat")}
          className={`w-1/4 relative inline-flex h-12 overflow-hidden rounded-lg p-[1px] ${focusStyles}`}
        >
          <span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
          <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-lg bg-slate-950 hover:bg-[#050c2e] transition-all duration-150 ease-in px-3 py-1 text-md font-bold text-white backdrop-blur-3xl">
            Start Chat
          </span>
        </button>
      </div>
    </HeroHighlight>
  );
};

export default HomePage;
