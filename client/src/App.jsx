import { BrowserRouter, Route, Routes } from "react-router-dom";
import { HomePage, ChatPage } from "./pages";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />}></Route>
        <Route path="/chat" element={<ChatPage />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
