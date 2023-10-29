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
        print(messages)
        try:
            for timestamp, message in messages.items():
                message_data = json.loads(message)
                chat = Chatlog(
                    auctionid= auctionid,
                    sender_id=message_data['user'],
                    message=message_data['context'],
                    timestamp=timestamp
                )
                db.session.add(chat)
            if db.session.commit():
                redis_client.delete(auctionid)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False