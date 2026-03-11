import { useState, useEffect } from "react";
import { api } from "../api";

export default function Agenda() {
    const [events, setEvents] = useState([]);
    const [error, setError] = useState("");

    const [name, setName] = useState("");
    const [datetime, setDatetime] = useState("");
    const [duration, setDuration] = useState("");
    const [description, setDescription] = useState("");
    const [repeats, setRepeats] = useState(false);
    const [repeatinterval, setRepeatInterval] = useState(0);

    useEffect(() => {
        loadEvents();
    }, []);

    const loadEvents = async () => {
        try {
            const data = await api.getEvents();
            setEvents(data);
        } catch (err) {
            console.error("Failed to load events:", err);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        try {
            await api.createEvent({
                name: name,
                datetime: datetime,
                duration: Number(duration),
                description: description,
                repeats: repeats,
                repeat_interval: Number(repeatinterval),
            });
            
            setName("");
            setDatetime("");
            setDuration("");
            setDescription("");
            setRepeats(false);
            setRepeatInterval(0);
            loadEvents();
        
        } catch (err) {
            setError(err.message);
        }
    };

    const handleDelete = async (id) => {
        await api.deleteEvent(id);
        loadEvents();
    };

    return (<div style={{ maxWidth: "800px", margin: "0 auto", padding: "20px", fontFamily: "sans-serif" }}>
      <h1>My Agenda</h1>

      <div style={{ background: "#f5f5f5", padding: "20px", borderRadius: "8px", marginBottom: "20px" }}>
        <h2>New Event</h2>
        {error && <p style={{ color: "red", fontWeight: "bold" }}>⚠️ {error}</p>}
        
        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          <input 
            type="text" 
            placeholder="Event Name" 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
            required 
          />
          <input 
            type="datetime-local" 
            value={datetime} 
            onChange={(e) => setDatetime(e.target.value)} 
            required 
          />
          <input 
            type="number" 
            placeholder="Duration (minutes)" 
            value={duration} 
            onChange={(e) => setDuration(e.target.value)} 
            required 
          />
          <textarea 
            placeholder="Description (Optional)" 
            value={description} 
            onChange={(e) => setDescription(e.target.value)} 
          />
          <button type="submit" style={{ padding: "10px", background: "#007BFF", color: "white", border: "none", cursor: "pointer", borderRadius: "4px" }}>
            Add Event
          </button>
        </form>
      </div>

      <div>
        <h2>Upcoming Events</h2>
        {events.length === 0 ? (
          <p>No scheduled events.</p>
        ) : (
          <ul style={{ listStyle: "none", padding: 0 }}>
            {events.map((event) => (
              <li key={event.id} style={{ border: "1px solid #ddd", padding: "15px", marginBottom: "10px", borderRadius: "5px", display: "flex", justifyContent: "space-between" }}>
                <div>
                  <strong>{event.name}</strong>
                  <p style={{ margin: "5px 0", color: "#666", fontSize: "14px" }}>
                    📅 {new Date(event.datetime).toLocaleString()} ⏳ {event.duration} min
                  </p>
                  <p style={{ margin: 0 }}>{event.description}</p>
                </div>
                <button 
                  onClick={() => handleDelete(event.id)} 
                  style={{ background: "#DC3545", color: "white", border: "none", padding: "5px 10px", cursor: "pointer", borderRadius: "4px", height: "fit-content" }}>
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}