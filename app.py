from flask import Flask, jsonify, request

app = Flask(__name__)

# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory data store
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# --- HELPER FUNCTION ---
def find_event(event_id):
    """Helper to find an event by ID or return None."""
    return next((e for e in events if e.id == event_id), None)

# --- ROUTES ---

@app.route('/')
def index():
    """Welcome message at the root route."""
    return jsonify({"message": "Welcome to the Events API!"})

@app.route('/events', methods=['GET'])
def get_events():
    """Return all events as a JSON array."""
    return jsonify([event.to_dict() for event in events]), 200

@app.route('/events', methods=['POST'])
def create_event():
    """Create a new event from JSON input."""
    data = request.get_json()

    # Validation: Check if title exists
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400

    # Generate a new ID based on the last item
    new_id = events[-1].id + 1 if events else 1
    new_event = Event(new_id, data['title'])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

@app.route('/events/<int:id>', methods=['PATCH'])
def update_event(id):
    """Update the title of an existing event by ID."""
    event = find_event(id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    # Update title if it exists in the request body
    if 'title' in data:
        event.title = data['title']

    return jsonify(event.to_dict()), 200

@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    """Remove an event from the list by ID."""
    global events  # Needed to modify the list variable itself
    event = find_event(id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    events = [e for e in events if e.id != id]
    return jsonify({"message": "Event deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)