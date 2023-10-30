import json
from flask import request
from flask_socketio import emit, join_room, leave_room
from datetime import datetime

from app.services.auction_service import AuctionService
from app.services.auth_service import AuthService
from app.services.sched_service import SchedService


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
            message = f"{id}님이 경매에 참여하였습니다."
            message_data = {"user": id, "context": message}
            emit_message(room, message_data)
        else:
            message_data = '올바른 사용자가 아닙니다.'
            emit_system(room, message_data)

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
        message = f"{id}님이 방을 나갔습니다."
        message_data = {"user": id, "context": message}
        emit_message(room, message_data)

    @socketio.on("message", namespace="/chat")
    def handle_message(data):
        authorization_header = request.headers.get('Authorization')
        auth_result = AuthService.authenticate_request(authorization_header)
        if isinstance(auth_result, dict):
            return auth_result

        id = auth_result
        room = data["room"]
        message = data["message"]

        if message.startswith("#"):
            try:
                price_now = int(message[1:])
                if AuctionService().countupAuctionPrice(room, price_now, id):
                    message = f"{id}님이 {price_now}로 성공적으로 입찰하였습니다."
                    message_data = {"user": id, "context": message}
                    message_data_str = json.dumps(message_data)
                    save_message_to_redis(room, message_data_str)
                    emit_message(room, message_data)
                else:
                    message = f"{price_now}로 입찰실패하였습니다. 금액을 확인 후 시도해 주세요."
                    message_data = {"user": id, "context": message}
                    message_data_str = json.dumps(message_data)
                    save_message_to_redis(room, message_data_str)
                    emit_system(room, message_data)
            except ValueError:
                message = "숫자값을 입력하세요"
        else:
            message_data = {"user": id, "context": message}
            message_data_str = json.dumps(message_data)
            save_message_to_redis(room, message_data_str)
            emit_message(room, message_data)

    @socketio.on("getmessage", namespace="/chat")
    def get_messages(data):
        room = data["room"]
        messages = redis_client.hgetall(room)
        sorted_messages = SchedService.sorted_redis_messages(messages)
        mysql = AuctionService.getChatlogMysql(room)
        result = {}
        for item in mysql:
            timestamp = item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            user = item['sender_id']
            context = item['message']
            result[timestamp] = {'user': user, 'context': context}
        result.update({k: v for k, v in sorted_messages.items()})
        emit("system", result, to=room)

    

    def save_message_to_redis(room, message_data_str):
        '''Redis로 메시지 저장'''
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        redis_client.hset(room, current_time, message_data_str)

    def emit_message(room, message_data):
        '''메시지 이벤트로 보내기'''
        emit("message", message_data, to=room)

    def emit_system(room, message_data):
        '''시스템 이벤트로 보내기'''
        emit("system", message_data, to=room)
