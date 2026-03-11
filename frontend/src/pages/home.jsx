import Agenda from "../components/agenda";
import ChatBox from "../components/chat";

export default function Home() {
  return (
    <div style={{ 
      display: "flex", 
      gap: "30px", 
      padding: "20px", 
      maxWidth: "1200px", 
      margin: "0 auto",
      fontFamily: "sans-serif"
    }}>
      
      <div style={{ flex: 2 }}>
        <Agenda />
      </div>

      <div style={{ 
        flex: 1, 
        backgroundColor: "#f9f9f9", 
        padding: "20px", 
        borderRadius: "8px",
        border: "1px solid #ddd",
        height: "fit-content"
      }}>
        <h2>AI Assistant</h2>
        <ChatBox />
      </div>

    </div>
  );
}