import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CreateUser from "./pages/CreateUser";
import UserDocuments from "./pages/UserDocuments";
import UploadDocuments from "./pages/UploadDocuments";
import Navbar from "./components/Navbar";
import ProtectedLayout from "./layouts/ProtectedLayout";
import ChatTopic from "./pages/ChatTopic";
import Admin from "./pages/Admin"
import Documents from "./pages/Documents";

function AppRoutes() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />

        <Route path="/dashboard" element={<ProtectedLayout><Dashboard /></ProtectedLayout>} />
        <Route path="/create-user" element={<ProtectedLayout><CreateUser /></ProtectedLayout>} />
        <Route path="/documents" element={<ProtectedLayout><Documents /></ProtectedLayout>} />
        <Route path="/upload-documents" element={<ProtectedLayout><UploadDocuments /></ProtectedLayout>} />
        <Route path="/chat/topics/:topicId" element={<ProtectedLayout> <ChatTopic /> </ProtectedLayout>} />
        <Route path="/admin" element={<ProtectedLayout> <Admin /> </ProtectedLayout>} />
      </Routes>
    </Router>
  );
}

export default AppRoutes;
