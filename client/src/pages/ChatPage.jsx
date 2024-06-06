const ChatPage = () => {
  return (
    <div className="flex flex-col h-screen mx-auto">
      <div className="px-20 py-14">
        <h1 className="text-4xl font-bold mb-4">Chat with Medical LLM</h1>
        <p className="text-lg mb-4">
          Here, users can chat with the Medical LLM.
        </p>

        <div className="w-full mx-auto">
          <textarea
            className="w-full bg-gray-100 border border-gray-300 rounded-lg p-4 mb-4 resize-none"
            rows="8"
            placeholder="Type your message here..."
          ></textarea>
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
