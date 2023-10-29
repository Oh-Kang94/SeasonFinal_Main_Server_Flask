from flask_restx import Resource, marshal, fields
from flask import request
from ..models.ApiModel import Auction_fields, Bidded_fields
from ..services.sched_service import SchedService
from ..config.Config import api
from flask_jwt_extended import jwt_required


def sched_routes(sched_ns, redis_client):
    @sched_ns.route("/")
    class Sched(Resource):
        def get(self):
            result = []
            keys = redis_client.keys('*')
            hash_keys = []
            for key in keys:
                if redis_client.type(key) == 'hash':
                    hash_keys.append(key)
            for key in hash_keys:
                print(key)
                if not SchedService.save_redis_to_mysql(key, redis_client):
                    result.append(key)
            if not result:  # 빈 리스트인 경우
                with open('faillist.txt', 'w') as file:
                    file.write('')
                with open('faillist.txt', 'a') as file:
                    file.write("success")
                return {'message': "Good!"}
            else:
                with open('faillist.txt', 'w') as file:
                    file.write('')
                with open('faillist.txt', 'a') as file:
                    file.write(str(result) + '\n')
                return {'message': f'Failed list {result}'}
