import { useState } from "react";

const ChatPage = () => {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const handleSend = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/chat/", {
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
    }
  };

  return (
    <div className="flex flex-col h-screen w-full mx-auto">
      <div className="px-20 py-14">
        <h1 className="text-4xl font-bold mb-4">Chat with Medical LLM</h1>
        <p className="text-lg mb-4">
          Ask questions about your health, get advice, and more.
          <br />
          The LLM is trained to specifically help you with your health concerns.
        </p>

        <div className="w-full mx-auto flex flex-col items-center mb-56">
          <textarea
            className="w-full max-w-3xl text-black bg-gray-100 border border-gray-300 rounded-lg p-4 mb-4 resize-none"
            rows="8"
            placeholder="Type your message here..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          ></textarea>
          <button
            className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4 transition-all duration-150 ease-in"
            onClick={handleSend}
          >
            Send
          </button>
          {response && (
            <div className="w-full max-w-3xl text-black mt-4 p-4 bg-gray-100 border border-gray-300 rounded-lg break-words h-48 overflow-y-auto">
              {response}
            </div>
          )}
        </div>

        <button
          className="w-1/4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4 transition-all duration-150 ease-in"
          onClick={() => {
            window.location.href = "/";
          }}
        >
          Back
        </button>
      </div>
    </div>
  );
};

export default ChatPage;
