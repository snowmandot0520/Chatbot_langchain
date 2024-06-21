import { useState } from "react";
import { HeroHighlight } from "../components";

const ChatPage = () => {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    try {
      setIsLoading(true);
      const res = await fetch("/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await res.json();
      setResponse(data.message);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const focusStyles =
    "focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50";

  return (
    <HeroHighlight>
      <div className="relative flex flex-col h-screen w-full mx-auto overflow-hidden font-mono">
        <div className="px-20 py-14 flex-grow">
          <h1 className="text-4xl font-bold mb-4">Chat with Medical LLM</h1>
          <p className="text-md mb-4">
            Ask questions about your health, get advice, and more.
            <br />
            The LLM is trained to specifically help you with your health
            concerns.
          </p>

          <div className="w-full mx-auto flex flex-col">
            <textarea
              className="w-full max-w-3xl text-black bg-gray-100 border border-gray-300 rounded-lg p-4 mb-4 resize-none"
              rows="8"
              placeholder="Type your message here..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            ></textarea>
            <button
              onClick={handleSend}
              className={`w-[765px] relative inline-flex h-12 overflow-hidden rounded-lg p-[1px] ${focusStyles}`}
            >
              <span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
              <span className="text-md font-mono inline-flex h-full w-full cursor-pointer items-center justify-center rounded-lg bg-slate-950 hover:bg-[#050c2e] transition-all duration-150 ease-in px-3 py-1 font-bold text-white backdrop-blur-3xl">
                {isLoading ? (
                  <div className="flex items-center justify-center">
                    <div className="w-5 h-5 border-4 border-t-4 border-t-white border-[#050c2e] rounded-full animate-spin"></div>
                    <span className="ml-2">Loading...</span>
                  </div>
                ) : (
                  "Send"
                )}
              </span>
            </button>
            {response && (
              <div className="w-full max-w-3xl text-black mt-4 p-4 bg-gray-100 border border-gray-300 rounded-lg break-words h-72 overflow-y-auto">
                {response}
              </div>
            )}
          </div>
        </div>
      </div>
      <button
        className={`fixed bottom-6 right-8 h-10 w-36 inline-flex h-10 overflow-hidden rounded-lg p-[1px] font-mono ${focusStyles}`}
        onClick={() => (window.location.href = "/")}
      >
        <span className="absolute inset-[-1000%] animate-[spin_2s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2CBFF_0%,#393BB2_50%,#E2CBFF_100%)]" />
        <span className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-lg bg-slate-950 hover:bg-[#050c2e] transition-all duration-150 ease-in px-3 py-1 text-md font-bold text-white backdrop-blur-3xl">
          Back
        </span>
      </button>
    </HeroHighlight>
  );
};

export default ChatPage;
