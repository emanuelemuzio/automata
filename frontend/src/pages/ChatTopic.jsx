import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchWithAuth } from "../api/authService";
import "../styles/ChatTopic.css";

function ChatTopic() {
  const { topicId } = useParams();
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMessages(); 
  }, [topicId]);

  const fetchMessages = async () => {
    try {
      const response = await fetchWithAuth(`/chat/history?topic_id=${topicId}`);
      if (!response.ok) throw new Error("Errore nel recupero dei messaggi");

      const data = await response.json();
      setMessages(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleSend = async () => {
    if (!question.trim()) return;

    const newMessages = [...messages, { sender: "user", text: question }];
    setMessages(newMessages);
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetchWithAuth("/chat/question", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, topic_id: topicId }),
      });

      const data = await response.json();
      newMessages.push({ sender: "ai", text: data.answer });

      setMessages(newMessages);
    } catch (error) {
      console.error("Errore nella chat:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h2>Topic: {topicId}</h2>

      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.sender}`}>
            <span>{msg.sender === "user" ? "🧑" : "🤖"}</span> {msg.text}
          </div>
        ))}
        {loading && <div className="chat-message ai">Digitando...</div>}
      </div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="Scrivi una domanda..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend} disabled={!question.trim()}>Invia</button>
      </div>
    </div>
  );
}

export default ChatTopic;
