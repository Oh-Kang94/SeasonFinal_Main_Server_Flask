import json
from flask_socketio import emit, send, join_room, leave_room
from datetime import datetime

def chat_routes(socketio, redis_client):
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
        }
        message_data_str = json.dumps(message_data) 
        redis_client.hset(room, message_data["timestamp"], message_data_str)
        emit("message", message_data, to=room)

    @socketio.on("getmessage", namespace="/chat")
    def get_messages(data):
        room = data["room"]
        messages = redis_client.hgetall(room)
        emit("message" ,{k: json.loads(v) for k, v in messages.items()})