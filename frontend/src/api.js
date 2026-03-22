const API_URL = "http://127.0.0.1:8000/api/agenda";

export const api = {
    getEvents: async () => {
        const response = await fetch(`${API_URL}/events`);
        
        if (!response.ok) {
            console.error("Failed to load events. Status:", response.status);
            return []; 
        }

        return response.json();
    },

    createEvent: async (eventData) => {
        const response = await fetch(`${API_URL}/events`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(eventData),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to create event");
        }
        return response.json();
    },

    deleteEvent: async (id) => {
        const response = await fetch(`${API_URL}/events/${id}`, {
            method: "DELETE",
        });

        if (!response.ok) 
            console.error("Failed to delete event. Status:", response.status);
        
        return response.json();
    },

    getTasks: async () => {
        const response = await fetch(`${API_URL}/tasks`);
        
        if (!response.ok) {
            console.error("Failed to load tasks. Status:", response.status);
            return []; 
        }

        return response.json();
    },

    createTask: async (taskData) => {
        const response = await fetch(`${API_URL}/tasks`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(taskData),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to create task");
        }
        return response.json();
    },

    deleteTask: async (id) => {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: "DELETE",
        });

        if (!response.ok) 
            console.error("Failed to delete task. Status:", response.status);
        
        return response.json();
    }
};