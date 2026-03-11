const API_URL = "http://127.0.0.1:8000/api/agenda";

export const api = {
    getEvents: async () => {
        const response = await fetch(`${API_URL}/`);
        
        if (!response.ok) {
            console.error("Failed to load events. Status:", response.status);
            return []; 
        }

        return response.json();
    },

    createEvent: async (eventData) => {
        const response = await fetch(`${API_URL}/`, {
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
    }
};