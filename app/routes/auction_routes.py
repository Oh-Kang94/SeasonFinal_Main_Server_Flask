from flask_restx import Resource, marshal, fields
from flask import request
from ..models.ApiModel import Auction_fields
from ..services.auction_service import AuctionService
from ..services.auth_service import AuthService
from ..config.Config import api
from flask_jwt_extended import jwt_required


def auction_routes(review_ns, auth_ns):
    authService = AuthService()

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
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            data = api.payload
            result = AuctionService.create_auction(
                data, id=id)
            if result:
                return {'message': 'Review created successfully', 'result': marshal(result, Auction_fields), "socekturl": f"ws://127.0.0.1:18712/{result.auctionid}"}, 200
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
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            data = api.payload
            result = AuctionService.create_auction(
                data, id=id)
            if result:
                return {'message': 'Review created successfully', 'result': marshal(result, Auction_fields)}, 200
            else:
                return {'message': 'Already wrote Review'}, 500
