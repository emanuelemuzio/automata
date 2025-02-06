import { Navigate, useLocation } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import Sidebar from "../components/Sidebar";
import "../styles/ProtectedLayout.css";

function ProtectedLayout({ children }) {
  const isAuthenticated = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return (
    <div className="protected-container">
      <Sidebar />
      <div className="protected-content">{children}</div>
    </div>
  );
}

export default ProtectedLayout;
