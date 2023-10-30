import json
from flask import request
from flask_socketio import emit, join_room, leave_room
from datetime import datetime

from app.services.auction_service import AuctionService
from app.services.auth_service import AuthService

def chat_routes(socketio, redis_client):
    @socketio.on("join", namespace="/chat")
    def joined_room(data):
        authorization_header = request.headers.get('Authorization')
        auth_result = AuthService.authenticate_request(
            authorization_header)
        if isinstance(auth_result, dict):
            return auth_result
        id = auth_result
        room = data["room"]
        if AuctionService.select_one_ongoing_auction(room):
            join_room(room)
            AuctionService().countupAuctionView(room)
            emit("message", f"{id}님이 경매에 참여하였습니다.", to=room)
        else:
            emit("system", f"Rejected")

    @socketio.on("leave", namespace="/chat")
    def leaved_room(data):
        room = data["room"]
        authorization_header = request.headers.get('Authorization')
        auth_result = AuthService.authenticate_request(
            authorization_header)
        if isinstance(auth_result, dict):
            return auth_result
        id = auth_result
        leave_room(room)
        emit("message", f"{id}님이 방을 나갔습니다.", to=room)

    @socketio.on("message", namespace="/chat")
    def handle_message(data):
        authorization_header = request.headers.get('Authorization')
        auth_result = AuthService.authenticate_request(
            authorization_header)
        if isinstance(auth_result, dict):
            return auth_result
        id = auth_result
        room = data["room"]
        message = data["message"]
        if message.startswith("#"):
            # 으로 시작한다면
            price_now = message[1:]  # '#' 문자를 제외한 서비스 이름 추출
            try:
                price_now = int(price_now)
                if AuctionService().countupAuctionPrice(room, price_now, id):
                    message = f"{id}님이 {price_now}로 성공적으로 입찰하였습니다."
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message_data = {
                        "user": id,
                        "context": message,
                    }
                    message_data_str = json.dumps(message_data) 
                    redis_client.hset(room, current_time, message_data_str)
                    emit("message", message_data, to=room)
                else:
                    message = f"{price_now}로 입찰실패하였습니다. 금액을 확인 후 시도해 주세요."
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message_data = {
                        "user": id,
                        "context": message,
                    }
                    message_data_str = json.dumps(message_data) 
                    emit("system", message_data, to=room)
            except ValueError:
                message = "숫자값을 입력하세요"
        

    @socketio.on("getmessage", namespace="/chat")
    def get_messages(data):
        room = data["room"]
        messages = redis_client.hgetall(room)
        mysql = AuctionService.getChatlogMysql(room)
        result = {}
        for item in mysql:
            timestamp = item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            user = item['sender_id']
            context = item['message']
            result[timestamp] = {'user': user, 'context': context}
        result.update({k: json.loads(v) for k, v in messages.items()})
        emit("system" ,result, to=room)