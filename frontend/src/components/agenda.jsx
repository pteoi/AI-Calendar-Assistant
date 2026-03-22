import { useState, useEffect } from "react";
import { api } from "../api";
import ChatBox from "./chat";

export default function Agenda() {
  const [activeTab, setActiveTab] = useState("events");
  const [error, setError] = useState("");


  const [events, setEvents] = useState([]);
  const [name, setName] = useState("");
  const [datetime, setDatetime] = useState("");
  const [duration, setDuration] = useState("");
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");
  const [repeats, setRepeats] = useState(false);
  const [repeatinterval, setRepeatInterval] = useState(0);
  const [repeatsUntil, setRepeatsUntil] = useState("");

  const [tasks, setTasks] = useState([]);
  const [taskName, setTaskName] = useState("");
  const [taskDeadline, setTaskDeadline] = useState("");
  const [taskDescription, setTaskDescription] = useState("");

  const loadEvents = async () => {
    try {
      const data = await api.getEvents();
      setEvents(data);
    } catch (err) {
      console.error("Failed to load events:", err);
    }
  };

  const loadTasks = async () => {
    try {
      const data = await api.getTasks(); 
      setTasks(data);
    } catch (err) {
      console.error("Failed to load tasks:", err);
    }
  };

  const refreshAllData = () => {
    loadEvents();
    loadTasks();
  };

  useEffect(() => {
    refreshAllData();
  }, []);

  const handleEventSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.createEvent({
        name, datetime, duration: Number(duration), location, description,
        repeats, repeat_interval: Number(repeatinterval), repeats_until: repeatsUntil || undefined
      });
      
      setName(""); setDatetime(""); setDuration(""); setLocation(""); setDescription(""); setRepeats(false); setRepeatInterval(0); setRepeatsUntil("");
      loadEvents();
    } catch (err) { setError(err.message); }
  };

  const handleTaskSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await api.createTask({
        name: taskName, deadline: taskDeadline, description: taskDescription
      });
      setTaskName(""); setTaskDeadline(""); setTaskDescription("");
      loadTasks();
    } catch (err) { setError(err.message); }
  };

  const handleDeleteEvent = async (id) => {
    await api.deleteEvent(id);
    loadEvents();
  };

  const handleDeleteTask = async (id) => {
    await api.deleteTask(id);
    loadTasks();
  };

  const tabStyle = (tabName) => ({
    padding: "10px 20px",
    cursor: "pointer",
    border: "none",
    borderBottom: activeTab === tabName ? "3px solid #007BFF" : "3px solid transparent",
    background: "transparent",
    fontWeight: "bold",
    fontSize: "16px",
    color: activeTab === tabName ? "#007BFF" : "#666"
  });

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "20px", fontFamily: "sans-serif" }}>
      <h1>Calendar</h1>

      <div style={{ display: "flex", gap: "20px", borderBottom: "1px solid #ddd", marginBottom: "20px" }}>
        <button style={tabStyle("events")} onClick={() => setActiveTab("events")}>📅 Events</button>
        <button style={tabStyle("tasks")} onClick={() => setActiveTab("tasks")}>✅ Tasks</button>
      </div>

      <div style={{ display: "flex", gap: "30px", flexWrap: "wrap" }}>
        
        <div style={{ flex: "2", minWidth: "300px" }}>
          {error && <p style={{ color: "red", fontWeight: "bold" }}>⚠️ {error}</p>}

          {activeTab === "events" && (
            <>
              <div style={{ background: "#f5f5f5", padding: "20px", borderRadius: "8px", marginBottom: "20px" }}>
                <h2>New Event (Manual)</h2>
                <form onSubmit={handleEventSubmit} style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                  <input type="text" placeholder="Event Name" value={name} onChange={(e) => setName(e.target.value)} required />
                  <div style={{ display: "flex", gap: "10px" }}>
                    <input type="datetime-local" value={datetime} onChange={(e) => setDatetime(e.target.value)} required style={{ flex: 1 }} />
                    <input type="number" placeholder="Duration (min)" value={duration} onChange={(e) => setDuration(e.target.value)} required style={{ flex: 1 }} />
                  </div>
                  <input type="text" placeholder="Location (Optional)" value={location} onChange={(e) => setLocation(e.target.value)} />
                  <textarea placeholder="Description (Optional)" value={description} onChange={(e) => setDescription(e.target.value)} />
                  <button type="submit" style={{ padding: "10px", background: "#007BFF", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Add Event</button>
                </form>
              </div>

              <h2>Upcoming Events</h2>
              {events.length === 0 ? <p>No scheduled events.</p> : (
                <ul style={{ listStyle: "none", padding: 0 }}>
                  {events.map((event) => (
                    <li key={event.id} style={{ border: "1px solid #ddd", padding: "15px", marginBottom: "10px", borderRadius: "5px", display: "flex", justifyContent: "space-between" }}>
                      <div>
                        <strong>{event.name}</strong>
                        <p style={{ margin: "5px 0", color: "#666", fontSize: "14px" }}>
                          📅 {new Date(event.datetime).toLocaleString()} ⏳ {event.duration} min
                        </p>

                        {event.location && <p style={{ margin: "0 0 5px 0", fontSize: "14px", color: "#17a2b8" }}>📍 {event.location}</p>}
                        <p style={{ margin: 0 }}>{event.description}</p>
                      </div>
                      <button onClick={() => handleDeleteEvent(event.id)} style={{ background: "#DC3545", color: "white", border: "none", padding: "5px 10px", borderRadius: "4px", cursor: "pointer", height: "fit-content" }}>Delete</button>
                    </li>
                  ))}
                </ul>
              )}
            </>
          )}

          {activeTab === "tasks" && (
            <>
              <div style={{ background: "#f5f5f5", padding: "20px", borderRadius: "8px", marginBottom: "20px" }}>
                <h2>New Task (Manual)</h2>
                <form onSubmit={handleTaskSubmit} style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                  <input type="text" placeholder="Task Name" value={taskName} onChange={(e) => setTaskName(e.target.value)} required />
                  <input type="datetime-local" value={taskDeadline} onChange={(e) => setTaskDeadline(e.target.value)} required />
                  <textarea placeholder="Description (Optional)" value={taskDescription} onChange={(e) => setTaskDescription(e.target.value)} />
                  <button type="submit" style={{ padding: "10px", background: "#28A745", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Add Task</button>
                </form>
              </div>

              <h2>Pending Tasks</h2>
              {tasks.length === 0 ? <p>No pending tasks.</p> : (
                <ul style={{ listStyle: "none", padding: 0 }}>
                  {tasks.map((task) => (
                    <li key={task.id} style={{ border: "1px solid #ddd", borderLeft: "5px solid #28A745", padding: "15px", marginBottom: "10px", borderRadius: "5px", display: "flex", justifyContent: "space-between" }}>
                      <div>
                        <strong>{task.name}</strong>
                        <p style={{ margin: "5px 0", color: "#d9534f", fontSize: "14px", fontWeight: "bold" }}>
                          ⏰ Deadline: {new Date(task.deadline).toLocaleString()}
                        </p>
                        <p style={{ margin: 0 }}>{task.description}</p>
                      </div>
                      <button onClick={() => handleDeleteTask(task.id)} style={{ background: "#DC3545", color: "white", border: "none", padding: "5px 10px", borderRadius: "4px", cursor: "pointer", height: "fit-content" }}>Delete</button>
                    </li>
                  ))}
                </ul>
              )}
            </>
          )}
        </div>

        <div style={{ flex: "1", minWidth: "300px" }}>
          <h2>Schedule with AI</h2>
          <ChatBox onDataUpdated={refreshAllData} />
        </div>

      </div>
    </div>
  );
}