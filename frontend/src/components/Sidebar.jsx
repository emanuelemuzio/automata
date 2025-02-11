import { useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import "../styles/Sidebar.css";
import Logo from "../components/Logo";
import useBootstrapTooltip from "../hooks/useBootstrapTooltip";
import { fetchWithAuth } from "../api/authService";
import useAuth from "../hooks/useAuth";
import { Collapse } from "bootstrap";

function Sidebar() {
  const userRole = useAuth();
  const navigate = useNavigate();
  const [chats, setChats] = useState([]);
  const [creating, setCreating] = useState(false);
  const location = useLocation();
  const [topics, setTopics] = useState([]);
  useBootstrapTooltip();
  

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("token_type");
    navigate("/login");
  };

  useEffect(() => {
    fetchChats();
    fetchTopics();
  }, [location.pathname]);

  const fetchTopics = async () => {
    try {
      const response = await fetchWithAuth("/topic/by_user");
      if (!response.ok) throw new Error("Errore nel recupero dei topic");
      const data = await response.json();
      setTopics(data);

      if (data.length === 0) {
        const chatCollapse = document.getElementById("chat-collapse");
        if (chatCollapse && chatCollapse.classList.contains("show")) {
          const collapseInstance = Collapse.getOrCreateInstance(chatCollapse);
          collapseInstance.hide();
        }
      }
    } catch (error) {
      console.error("Errore nel recupero dei topic:", error);
    }
  };

  const fetchChats = async () => {
    try {
      const response = await fetchWithAuth("/topic/by_user");
      if (!response.ok) throw new Error("Errore nel recupero delle chat");

      const data = await response.json();
      setChats(data);
    } catch (error) {
      console.error("Errore nel recupero delle chat:", error);
    }
  };

  const handleCreateChat = async () => {
    setCreating(true);

    try {
      const response = await fetchWithAuth("/topic", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: "Nuova Chat" }),
      });

      if (!response.ok) throw new Error("Errore nella creazione della chat");

      const newChat = await response.json();
      setChats([...chats, newChat]);
      navigate(`/chat/topics/${newChat.id}`);
    } catch (error) {
      console.error("Errore durante la creazione della chat:", error);
    } finally {
      setCreating(false);
    }
  }; 

  return (

    <div className="d-flex flex-column flex-shrink-0 p-3 text-white bg-dark sidebar" >

      <ul className="nav nav-pills flex-column mb-auto">

        <li className="nav-item">
          <Link to="/" className="home-button nav-link">
            <Logo width="72" height="72" />
          </Link>
        </li>

        <li className={`nav-item ${location.pathname === "/dashboard" ? "active" : ""}`}>
          <Link to="/dashboard" className="nav-link">
            <i className="bi bi-speedometer me-2"></i>
            Dashboard
          </Link>
        </li>

        <li className={"mb-1"}>
          <button 
          className={`nav-link primary collapse show`} 
          data-bs-toggle={chats.length > 0 ? "collapse" : ""}
          data-bs-target={chats.length > 0 ? "#chat-collapse" : ""}
          aria-expanded="false"
          >
            <i className="bi bi-chat me-2"></i>
            Chat
          </button>
          <div className="collapse" id="chat-collapse">
            <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
              {chats.length > 0 ? (
                chats.map((chat) => (
                  <li key={chat.id}>
                    <Link to={`/chat/topics/${chat.id}`} className="link rounded">
                      {chat.name}
                    </Link>
                  </li>
                ))
              ) : (
                <li className="text-muted">Nessuna chat disponibile</li>
              )}
            </ul>
          </div>
        </li>

        {userRole.userRole === "ADMIN" && (
          <li className={`nav-item ${location.pathname === "/admin" ? "active" : ""}`}>
            <Link to="/admin" className="nav-link">
              <i className="bi bi-people me-2"></i>
              Amministrazione
            </Link>
          </li>
        )}

        <li className={`nav-item ${location.pathname === "/documents" ? "active" : ""}`}>
          <Link to="/documents" className="nav-link">
            <i className="bi bi-file-earmark-pdf me-2"></i>
            Documenti
          </Link>
        </li>

      </ul>

      <button className="btn btn-primary mb-2" onClick={handleCreateChat} disabled={creating}>
        <i className="bi bi-journal-plus me-2"></i>
        Nuova chat
      </button>
      <button className="btn btn-danger mb-2" onClick={handleLogout}>
        <i className="bi bi-box-arrow-in-left me-2"></i>
        Logout
      </button>
    </div>
  )
}

export default Sidebar;
