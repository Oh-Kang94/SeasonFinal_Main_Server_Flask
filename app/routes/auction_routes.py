from flask_restx import Resource, marshal, fields
from flask import request, session
from ..models.ApiModel import Auction_fields
from ..services.user_service import UsersService
from ..services.auction_service import AuctionService
from ..services.auth_service import Auth_Service
from ..config.Config import api
from flask_jwt_extended import jwt_required

def  auction_routes(review_ns, auth_ns):
    @review_ns.route('/')
    class CreateAuction(Resource):
        @jwt_required()
        @review_ns.doc(
            description='경매시작하기.',
            responses={
                401: 'Invalid token',
                400: 'Missing Authorization header',
                200: 'Success',
                500: 'Already wrote Review',
            })
        @auth_ns.doc(security='Bearer')
        @review_ns.expect(api.model('CreateReview', {
            'title': fields.String(description='movie_id integer', example='도미'),
            'content': fields.String(description='영화의 리뷰 내용', example='도미 굿'),
            'pic': fields.String(description='영화의 평점으로 Rating', example='asd.jpg'),
            'fish': fields.String(description='영화의 평점으로 Rating', example='도미'),
            'pricestart': fields.String(description='영화의 평점으로 Rating', example='10000'),
        }))
        def post(self):
            authorization_header = request.headers.get('Authorization')
            if authorization_header and authorization_header.startswith('Bearer '):
                decoded_token = Auth_Service.decode_token(authorization_header)
                if decoded_token:
                    # 여기서 'sub'는 사용자의 이메일 주소를 의미합니다.
                    id = decoded_token.get('sub')
                else:
                    return {'message': 'Invalid token'}, 401
            else:
                return {'message': "Invalid or missing Authorization header"}, 400
            data = api.payload
            
            result = AuctionService.create_auction(
                data, id=id)
            if result:
                return {'message': 'Review created successfully', 'result': marshal(result, Auction_fields)}, 200
            else:
                return {'message': 'Already wrote Review'}, 500
    
    @review_ns.route('/<string:auctionid>')
    class EditAuction(Resource):
        @jwt_required()
        @review_ns.doc(
            description='경매 수정하기.',
            responses={
                401: 'Invalid token',
                400: 'Missing Authorization header',
                200: 'Success',
                500: 'Already wrote Review',
            })
        @auth_ns.doc(security='Bearer')
        @review_ns.expect(api.model('CreateReview', {
            'title': fields.String(example='도미'),
            'content': fields.String(example='도미 굿'),
            'pic': fields.String(example='asd.jpg'),
            'fish': fields.String(example='도미'),
            'pricestart': fields.String(example='10000'),
        }))
        def put(self):
            authorization_header = request.headers.get('Authorization')
            if authorization_header and authorization_header.startswith('Bearer '):
                decoded_token = Auth_Service.decode_token(authorization_header)
                if decoded_token:
                    # 여기서 'sub'는 사용자의 이메일 주소를 의미합니다.
                    id = decoded_token.get('sub')
                else:
                    return {'message': 'Invalid token'}, 401
            else:
                return {'message': "Invalid or missing Authorization header"}, 400
            data = api.payload

            result = AuctionService.create_auction(
                data, id=id)
            if result:
                return {'message': 'Review created successfully', 'result': marshal(result, Auction_fields)}, 200
            else:
                return {'message': 'Already wrote Review'}, 500