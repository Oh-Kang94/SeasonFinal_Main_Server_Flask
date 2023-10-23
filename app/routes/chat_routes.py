from flask_socketio import emit, send, join_room, leave_room
from datetime import datetime

def chat_routes(socketio):
    @socketio.on("join", namespace="/chat")
    def joined_room(data):
        room = data["room"]
        join_room(room)
        emit("message", f"User joined room {room}", to=room)

    @socketio.on("leave", namespace="/chat")
    def leaved_room(data):
        room = data["room"]
        leave_room(room)
        emit("message", f"User left room {room}", to=room)

    @socketio.on("message", namespace="/chat")
    def handle_message(data):
        room = data["room"]
        message = data["message"]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_data = {
            "message": message,
            "timestamp": current_time
        }
        # redis_client.hset(room, message_data["timestamp"], message_data)
        emit("message", message_data, to=room)