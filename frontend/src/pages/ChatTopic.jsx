import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchWithAuth } from "../api/authService";
import "../styles/ChatTopic.css";

function ChatTopic() {
  const { topicId } = useParams();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sending, setSending] = useState(false);

  useEffect(() => {
    fetchMessages();
  }, [topicId]);

  const fetchMessages = async () => {
    setLoading(true);
    try {
      const response = await fetchWithAuth(`/chat/messages?topic_id=${topicId}`);
      if (!response.ok) throw new Error("Errore nel recupero dei messaggi");

      const data = await response.json();

      const formattedMessages = data.flatMap((msg) => [
        { sender: "user", text: msg.question, timestamp: msg.created_at },
        { sender: "bot", text: msg.answer, timestamp: msg.created_at },
      ]);

      setMessages(formattedMessages);
    } catch (error) {
      setError("Impossibile caricare i messaggi");
      console.error("Errore nella chat:", error);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim()) return;

    setSending(true);
    try {
      const response = await fetchWithAuth(`/chat/messages`, {
        method: "POST",
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

  if (loading) return <p>Caricamento chat...</p>;
  if (error) return <p className="text-danger">{error}</p>;

  return (
    <div className="container chat-container mt-4">
      <h2>Chat Topic #{topicId}</h2>

      {/* Area Messaggi */}
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

      {/* Input e Bottone di Invio */}
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
