import json
from flask_jwt_extended import jwt_required
from flask_socketio import emit, send, join_room, leave_room
from datetime import datetime

from app.services.auction_service import AuctionService

def chat_routes(socketio, redis_client):
    @socketio.on("join", namespace="/chat")
    def joined_room(data):
        room = data["room"]
        user = data["user"]
        join_room(room)
        AuctionService().countupAuctionView(room)
        emit("message", f"{user} joined room {room}", to=room)

    @socketio.on("leave", namespace="/chat")
    def leaved_room(data):
        room = data["room"]
        user = data["user"]
        leave_room(room)
        emit("message", f"{user} left room {room}", to=room)

    @socketio.on("message", namespace="/chat")
    def handle_message(data):
        room = data["room"]
        user = data["user"]
        message = data["message"]
        if message.startswith("#"):
            # 으로 시작한다면
            price_now = message[1:]  # '#' 문자를 제외한 서비스 이름 추출
            try:
                price_now = int(price_now)
                if AuctionService().countupAuctionPrice(room, price_now, user):
                    message = f"{price_now}로 성공적으로 입찰하였습니다."
                else:
                    message = f"{price_now}로 입찰실패하였습니다."
            except ValueError:
                message = "숫자값을 입력하세요"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_data = {
            "user": user,
            "context": message,
        }
        message_data_str = json.dumps(message_data) 
        redis_client.hset(room, current_time, message_data_str)
        emit("message", message_data, to=room)

    @socketio.on("getmessage", namespace="/chat")
    def get_messages(data):
        room = data["room"]
        messages = redis_client.hgetall(room)
        emit("message" ,{k: json.loads(v) for k, v in messages.items()}, to=room)