import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Sidebar.css";

function Sidebar() {
  const [isAdminOpen, setIsAdminOpen] = useState(false);
  const [isDocsOpen, setIsDocsOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("token_type");
    navigate("/login");
  };

  return (
    <aside className="sidebar">
      <Link to="/" className="home-button">Home</Link>

      <Link to="/dashboard" className="sidebar-link">Dashboard</Link>

      <div className="sidebar-menu">
        <button onClick={() => setIsAdminOpen(!isAdminOpen)}>
          Amministrazione
        </button>
        {isAdminOpen && (
          <div className="submenu">
            <Link to="/create-user">Crea utente</Link>
          </div>
        )}
      </div>

      <div className="sidebar-menu">
        <button onClick={() => setIsDocsOpen(!isDocsOpen)}>
          Documenti
        </button>
        {isDocsOpen && (
          <div className="submenu">
            <Link to="/user-documents">I tuoi documenti</Link>
            <Link to="/upload-documents">Carica documenti</Link>
          </div>
        )}
      </div>

      <button className="logout-button" onClick={handleLogout}>Logout</button>
    </aside>
  );
}

export default Sidebar;
