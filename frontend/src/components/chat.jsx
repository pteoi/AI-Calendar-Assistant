import { useState } from "react";

export default function ChatBox({ onDataUpdated }) {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const [messages, setMessages] = useState([
    { text: "Hi! I'm your AI assistant. Tell me what event you want to schedule.", sender: "ai" }
  ]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();

    setMessages((prev) => [...prev, { text: userMessage, sender: "user" }]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Error communicating with AI");
      }

      setMessages((prev) => [...prev, { text: data.reply, sender: "ai" }]);

      if (onDataUpdated) {
        onDataUpdated();
      }

    } catch (error) {
      setMessages((prev) => [...prev, { text: `❌ ${error.message}`, sender: "ai" }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "450px" }}>

      <div style={{
        flex: 1,
        overflowY: "auto",
        padding: "10px",
        border: "1px solid #ccc",
        borderRadius: "8px",
        marginBottom: "10px",
        backgroundColor: "#fff"
      }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === "user" ? "right" : "left", marginBottom: "10px" }}>
            <span style={{
              display: "inline-block",
              padding: "10px 14px",
              borderRadius: "15px",
              backgroundColor: msg.sender === "user" ? "#007BFF" : "#E9ECEF",
              color: msg.sender === "user" ? "#fff" : "#000",
              maxWidth: "85%",
              lineHeight: "1.4"
            }}>
              {msg.text}
            </span>
          </div>
        ))}

        {isLoading && (
          <div style={{ textAlign: "left", marginBottom: "10px" }}>
            <span style={{ display: "inline-block", padding: "10px 14px", borderRadius: "15px", backgroundColor: "#E9ECEF", fontStyle: "italic", color: "#666" }}>
              ⏳ Thinking...
            </span>
          </div>
        )}
      </div>

      <form onSubmit={handleSend} style={{ display: "flex", gap: "10px" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="E.g., Meeting with John tomorrow at 3 PM"
          style={{ flex: 1, padding: "10px", borderRadius: "4px", border: "1px solid #ccc" }}
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading}
          style={{
            padding: "10px 20px",
            backgroundColor: isLoading ? "#ccc" : "#28A745",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: isLoading ? "not-allowed" : "pointer",
            fontWeight: "bold"
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
}