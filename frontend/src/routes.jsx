import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CreateUser from "./pages/CreateUser";
import UserDocuments from "./pages/UserDocuments";
import UploadDocuments from "./pages/UploadDocuments";
import Navbar from "./components/Navbar";
import ProtectedLayout from "./layouts/ProtectedLayout";
import Chat from "./pages/Chat";
import ChatTopic from "./pages/ChatTopic";

function AppRoutes() {
  return (
    <Router>
      <Navbar />
      <Routes>
        {/* Pagine pubbliche */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />

        {/* Pagine protette con layout */}
        <Route path="/dashboard" element={<ProtectedLayout><Dashboard /></ProtectedLayout>} />
        <Route path="/create-user" element={<ProtectedLayout><CreateUser /></ProtectedLayout>} />
        <Route path="/user-documents" element={<ProtectedLayout><UserDocuments /></ProtectedLayout>} />
        <Route path="/upload-documents" element={<ProtectedLayout><UploadDocuments /></ProtectedLayout>} />
        <Route path="/chat" element={<ProtectedLayout><Chat /></ProtectedLayout>} />
        <Route path="/chat/topics/:topicId" element={<ChatTopic />} />
      </Routes>
    </Router>
  );
}

export default AppRoutes;
