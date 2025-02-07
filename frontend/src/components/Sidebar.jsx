import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Sidebar.css";
import Logo from "../components/Logo";
import useBootstrapTooltip from "../hooks/useBootstrapTooltip";
import { fetchWithAuth } from "../api/authService";

function Sidebar() {
  const navigate = useNavigate();
  const [chats, setChats] = useState([]);
  useBootstrapTooltip();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("token_type");
    navigate("/login");
  };

  useEffect(() => {
    fetchChats();
  }, []);

  const fetchChats = async () => {
    try {
      const response = await fetchWithAuth("/chat/topics");
      if (!response.ok) throw new Error("Errore nel recupero delle chat");

      const data = await response.json();
      setChats(data);
    } catch (error) {
      console.error("Errore nel recupero delle chat:", error);
    }
  };

  return (

    <div className="d-flex flex-column flex-shrink-0 p-3 text-white bg-dark" >

      <ul className="nav nav-pills flex-column mb-auto">

        <li className="nav-item">
          <Link to="/" className="home-button nav-link">
            <Logo width="72" height="72" />
          </Link>
        </li>

        <li className="nav-item">
          <Link to="/" className="nav-link text-white">
            Home
          </Link>
        </li>

        <li className={`nav-item ${location.pathname === "/documents" ? "active" : ""}`}>
          <Link to="/dashboard" className="nav-link">
            Dashboard
          </Link>
        </li>

        <li className={"mb-1"}>
          <button className={"nav-link text-white collapse show"} data-bs-toggle="collapse" data-bs-target="#chat-collapse" aria-expanded="false">
            Chat
          </button>
          <div className="collapse" id="chat-collapse">
            <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
              {chats.length > 0 ? (
                chats.map((chat) => (
                  <li key={chat.id}>
                    <Link to={`/chat/topics/${chat.id}`} className="link-light rounded">
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
      </ul>

      <button className="btn btn-danger" onClick={handleLogout}>Logout</button>
    </div>
  )
}

export default Sidebar;
