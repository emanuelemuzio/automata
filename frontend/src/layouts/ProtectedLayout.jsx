import { Navigate, useLocation } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import Sidebar from "../components/Sidebar";
import "../styles/ProtectedLayout.css";

function ProtectedLayout({ children }) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  return isLoading ? (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="spinner-border" role="status">
      </div>
    </div>
  ) : (
    isAuthenticated ? (
      <div className="protected-container">
        <Sidebar />
        <div className="protected-content">{children}</div>
      </div>
    ) : (
      <Navigate to="/login" state={{ from: location }} replace />
    )
  );
}

export default ProtectedLayout;
