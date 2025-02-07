import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchWithAuth } from "../api/authService";  // Assicurati che il percorso sia corretto
import "../styles/Chat.css";

function Chat() {
  const [topics, setTopics] = useState([]);
  const [newTopicName, setNewTopicName] = useState("");
  const [creatingTopic, setCreatingTopic] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchTopics();
  }, []);

  const fetchTopics = async () => {
    try {
      const response = await fetchWithAuth("/chat/topics");
      if (!response.ok) throw new Error("Errore nel recupero delle chat");

      const data = await response.json();
      setTopics(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleCreateTopic = async () => {
    if (!newTopicName.trim() || topics.length >= 10) return;
    setCreatingTopic(true);

    try {
      const response = await fetchWithAuth("/chat/topics", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newTopicName }),  // ✅ Invia il body corretto con "name"
      });

      if (!response.ok) throw new Error("Errore nella creazione della chat");

      const newTopic = await response.json();
      setTopics([...topics, newTopic]);
      setNewTopicName("");
    } catch (error) {
      console.error(error);
    } finally {
      setCreatingTopic(false);
    }
  };

  const handleTopicClick = (topicId) => {
    navigate(`/chat/topics/${topicId}`);
  };

  return (
    <div className="chat-page">
      <div className="chat-container">
        <h2>Le tue Chat</h2>

        {/* Form per creare una nuova chat */}
        {topics.length < 10 && (
          <div className="new-chat">
            <input
              type="text"
              placeholder="Nome della chat..."
              value={newTopicName}
              onChange={(e) => setNewTopicName(e.target.value)}
            />
            <button onClick={handleCreateTopic} disabled={!newTopicName.trim() || creatingTopic}>
              {creatingTopic ? "Creando..." : "➕ Crea"}
            </button>
          </div>
        )}

        {/* Tabella con l'elenco delle chat */}
        <table className="chat-table">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Azioni</th>
            </tr>
          </thead>
          <tbody>
            {topics.length > 0 ? (
              topics.map((topic) => (
                <tr key={topic.id}>
                  <td>{topic.name}</td>
                  <td>
                    <button className="view-chat" onClick={() => handleTopicClick(topic.id)}>
                      Vai alla Chat
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="2">Nessuna chat disponibile</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Chat;
