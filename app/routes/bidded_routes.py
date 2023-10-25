from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields, marshal
from ..config.Config import api
from ..services.bidded_service import BiddedService
from ..services.auth_service import AuthService
from ..models.ApiModel import Bidded_fields

def bidded_routes(bid_ns, auth_ns):
    authService = AuthService()
    biddedService = BiddedService()

    @bid_ns.route("/")
    class BiddedbyAll(Resource):
        @jwt_required()
        @bid_ns.doc(
            description='모든 입찰 확인 내역 보기',
            responses={
                402: "You're not Admin",
                401: 'Invalid token',
                400: 'Missing Authorization header',
                200: 'Success',
                500: 'No Bidded',
            })
        @auth_ns.doc(security='Bearer')
        def get(self):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            if id == "root":
                result = biddedService.select_auction_all()
                if result:
                    return {'message': 'Auction Loaded successfully', 'result': marshal(result, Bidded_fields)}, 200
                else:
                    return {'message': 'No Bidded'}, 500
            else:
                return {'message': "You're not Admin"}, 402
    
    @bid_ns.route("/<int:biddedid>")
    class Biddedbybidid(Resource):
        @jwt_required()
        @bid_ns.doc(
            description='입찰 번호로 입찰내역 확인하기',
            responses={
                200: 'Success',
                400: 'Missing Authorization header',
                401: 'Invalid token',
                402: "You can't access the other's data",
                500: 'No Bidded',
            })
        @auth_ns.doc(security='Bearer')
        def get(self, biddedid):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            result = biddedService.select_auction_query("biddedid", biddedid)
            result = marshal(result, Bidded_fields)
            if result:
                if result["buyerid"] == id:
                    return {'message': 'Auction Loaded successfully', 'result': result}, 200
                else:
                    return {'message': "You can't access the other's data"}, 402
            else:
                return {'message': 'No Bidded'}, 500

    @bid_ns.route("/user/<string:who>")
    class Biddedbybidid(Resource):
        @jwt_required()
        @bid_ns.doc(
            description='유저 id로 입찰내역 확인하기(buying, selling)',
            responses={
                200: 'Success',
                400: 'Missing Authorization header',
                401: 'Invalid token',
                402: "You can't access the other's data",
                500: 'No Bidded',
                403: 'Invalid request.'
            })
        @auth_ns.doc(security='Bearer')
        def get(self, who):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            if who == "buying":
                result = biddedService.select_auction_query("buyerid", id)
                result = marshal(result, Bidded_fields)
                if result:
                    return {'message': 'Auction Loaded successfully', 'result': result}, 200
                else:
                    return {'message': 'No Bidded'}, 500    
    
            
