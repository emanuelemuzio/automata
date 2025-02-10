import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchWithAuth } from "../api/authService";
import "../styles/ChatTopic.css";

function ChatTopic() {
  const { topicId } = useParams();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sending, setSending] = useState(false);
  const [topicName, setTopicName] = useState("Caricamento...");
  const [newTopicName, setNewTopicName] = useState("");
  const [editingTopicName, setEditingTopicName] = useState(false);

  useEffect(() => {
    fetchMessages();
  }, [topicId]);

  const fetchMessages = async () => {
    setLoading(true);
    try {
      const response = await fetchWithAuth(`/chat?topic_id=${topicId}`);
      if (!response.ok) throw new Error("Errore nel recupero dei messaggi");

      const data = await response.json();

      const formattedMessages = data.history.flatMap((msg) => [
        { sender: "user", text: msg.question, timestamp: msg.created_at },
        { sender: "bot", text: msg.answer, timestamp: msg.created_at },
      ]);

      setTopicName(data.topic.name);
      setNewTopicName(data.topic.name);
      setMessages(formattedMessages);
    } catch (error) {
      setError("Impossibile caricare i messaggi");
      console.error("Errore nella chat:", error);
      navigate("/dashboard");
    } finally {
      setLoading(false);
    }
  };

  const handleEditClick = () => {
    setEditingTopicName(true);
  };

  const sendMessage = async () => {
    if (!newMessage.trim()) return;

    setSending(true);
    try {
      const response = await fetchWithAuth(`/chat`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: newMessage, topic_id: parseInt(topicId) }),
      });

      if (!response.ok) throw new Error("Errore nella generazione della risposta");

      const generatedResponse = await response.json();

      setMessages([
        ...messages,
        { sender: "user", text: newMessage, timestamp: new Date().toISOString() },
        { sender: "bot", text: generatedResponse.answer, timestamp: new Date().toISOString() },
      ]);

      setNewMessage("");
    } catch (error) {
      console.error("Errore nell'invio del messaggio:", error);
    } finally {
      setSending(false);
    }
  };

  const handleBlurOrSubmit = async () => {
    setEditingTopicName(false);

    if (newTopicName.trim() && newTopicName !== topicName) {
      try {
        const response = await fetchWithAuth(`/topic?idx=${topicId}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: newTopicName }),
        });

        if (!response.ok) throw new Error("Errore nell'aggiornamento del topic");

        setTopicName(newTopicName);
      } catch (error) {
        console.error("Errore durante l'aggiornamento del nome del topic:", error);
      }
    }
  };

  const handleDeleteTopic = async () => {
    if (!window.confirm("Sei sicuro di voler eliminare questo topic? L'azione è irreversibile.")) return;

    try {
      const response = await fetchWithAuth(`/topic?idx=${topicId}`, {
        method: "DELETE",
      });

      if (!response.ok) throw new Error("Errore nella cancellazione del topic");

      navigate("/dashboard"); 
    } catch (error) {
      console.error("Errore durante l'eliminazione del topic:", error);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleBlurOrSubmit();
    }
  };

  if (loading) return <p>Caricamento chat...</p>;
  if (error) return <p className="text-danger">{error}</p>;

  return (
    <div className="container chat-container">
      {editingTopicName ? (
        <input
          type="text"
          className="form-control topic-input"
          value={newTopicName}
          onChange={(e) => setNewTopicName(e.target.value)}
          onBlur={handleBlurOrSubmit}
          onKeyDown={handleKeyDown}
          autoFocus
        />
      ) : (
        <div className="title-container">
          <h2 className="editable-title" >
            {topicName}
          </h2>
          <button title="Modifica" className="btn btn-sm rounded-pill btn-success" onClick={handleEditClick}>
            <i className="bi bi-pencil"></i>
          </button>
          <button title="Elimina" className="btn btn-sm rounded-pill btn-danger" onClick={handleDeleteTopic}>
            <i className="bi bi-trash"></i>
          </button>
        </div>

      )}

      <div className="chat-box">
        {messages.length > 0 ? (
          messages.map((msg, index) => (
            <div key={index} className={`message-container ${msg.sender === "user" ? "user-message-container" : "bot-message-container"}`}>
              <div className={`message ${msg.sender === "user" ? "user-message" : "bot-message"}`}>
                <strong>{msg.sender === "user" ? "Tu" : "Bot"}:</strong> {msg.text}
                <small className="timestamp">{new Date(msg.timestamp).toLocaleString()}</small>
              </div>
            </div>
          ))
        ) : (
          <p className="text-muted">Nessun messaggio ancora.</p>
        )}
      </div>

      <div className="input-group mt-3">
        <input
          type="text"
          className="form-control"
          placeholder="Scrivi un messaggio..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          disabled={sending}
        />
        <button className="btn btn-primary" onClick={sendMessage} disabled={sending}>
          {sending ? "Generando..." : "Invia"}
        </button>
      </div>
    </div>
  );
}

export default ChatTopic;
