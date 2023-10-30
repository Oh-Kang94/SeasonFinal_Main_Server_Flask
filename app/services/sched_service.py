import json
from sqlalchemy import desc, or_
from ..models.DBModel import Chatlog
from ..config.Config import db
from ..util.util import current_datetime

class SchedService:

    @staticmethod
    def save_redis_to_mysql(auctionid, redis_client):
        '''redis에 있는 정보 불러다 mysql에 저장하기'''
        messages = redis_client.hgetall(auctionid)
        message_data = SchedService.sorted_redis_messages(messages)
        try:
            for timestamp, message in message_data.items():
                chat = Chatlog(
                    auctionid= auctionid,
                    sender_id=message['user'],
                    message=message['context'],
                    timestamp=timestamp
                )
                db.session.add(chat)
                db.session.commit()
                fields = redis_client.hkeys(auctionid)
                for field in fields:
                    redis_client.hdel(auctionid, field)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    
    @staticmethod
    def sorted_redis_messages(messages):
        '''timestamp 별로 정렬'''
        sorted_messages = {}
        for timestamp_str, message_data_str in messages.items():
            message_data = json.loads(message_data_str)
            sorted_messages[timestamp_str] = message_data
        sorted_messages = dict(sorted(sorted_messages.items(), key=lambda item: item[0]))
        return sorted_messages