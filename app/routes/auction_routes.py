from flask_restx import Resource, marshal, fields
from flask import request
from ..models.ApiModel import Auction_fields, Bidded_fields
from ..services.auction_service import AuctionService
from ..services.auth_service import AuthService
from ..config.Config import api
from flask_jwt_extended import jwt_required
from apscheduler.schedulers.background import BackgroundScheduler

def auction_routes(auc_ns, auth_ns):
    authService = AuthService()
    auctionService = AuctionService()

    @auc_ns.route('/')
    class AuctionbyAll(Resource):
        @jwt_required()
        @auc_ns.doc(
            description='경매 열기.',
            responses={
                401: 'Invalid token',
                400: 'Missing Authorization header',
                200: 'Success',
                500: 'Already wrote Review',
            })
        @auth_ns.doc(security='Bearer')
        @auc_ns.expect(api.model('CreateAuction', {
            'title': fields.String(description='경매 제목', example='도미팝니당!'),
            'content': fields.String(description='경매 내용', example='도미 굿'),
            'pic': fields.String(description='경매 사진경로(Firebase)', example='asd.jpg'),
            'fish': fields.String(description='경매에 쓰일 물고기', example='도미'),
            'pricestart': fields.String(description='경매 시작가', example='10000'),
        }))
        def post(self):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            data = api.payload
            result = auctionService.create_auction(
                data, id=id)
            enddate = result.endeddate
            ### 경매가 시작되면 endeddate에 자연적으로 경매가 끝남
            sched = BackgroundScheduler(daemon=True)
            sched.add_job(auctionService.setCloseAuction, 'date', run_date=enddate, args=[result.auctionid])
            sched.start()
            if result:
                return {'message': 'Auction created successfully', 'result': marshal(result, Auction_fields)}, 200
            else:
                return {'message': 'Already wrote Auction'}, 500
            
        @auc_ns.doc(
            description='경매 불러오기.',
            responses={
                200: 'Success',
                500: 'No Auction ongoing',
            })
        def get(self):
            result = auctionService.select_all_auction()
            if result:
                return {'message': 'Auction Loaded successfully', 'result': marshal(result, Auction_fields)}, 200
            else:
                return {'message': 'No Auction Ongoing'}, 500

    @auc_ns.route('/<int:auctionid>')
    class AuctionbyOne(Resource):
        @auc_ns.doc(
            description= '진행중인 경매 정보 하나 가져오기',
            response={
                200: "Success",
                500: "Failed to get Auction"
            }
        )
        def get(self, auctionid):
            AuctionService().countupAuctionView(auctionid)
            result = auctionService.select_one_ongoing_auction(auctionid)
            if result:
                return {'message': 'Auction Loaded successfully', 'result': marshal(result, Auction_fields)}, 200
            else:
                return {'message': 'Failed to get Ongoing Auction'}, 500
            

        @jwt_required()
        @auc_ns.doc(
            description='경매 수정하기.',
            responses={
                401: 'Invalid token',
                400: 'Missing Authorization header',
                200: 'Success',
                500: 'Same as Before',
                501: "You're not Seller"
            })
        @auth_ns.doc(security='Bearer')
        @auc_ns.expect(api.model('UpdateAuction', {
            'title': fields.String(description='경매 제목', example='도미팝니당!'),
            'content': fields.String(description='경매 내용', example='도미 굿'),
            'pic': fields.String(description='경매 사진경로(Firebase)', example='asd.jpg'),
            'fish': fields.String(description='경매에 쓰일 물고기', example='도미'),
            'pricestart': fields.String(description='경매 시작가', example='10000'),
        }))
        def put(self, auctionid):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            data = api.payload
            if auctionService.select_is_seller(id, auctionid):
                result = auctionService.update_auction(
                    data, id, auctionid)
                if result:
                    return {'message': 'Auction updated successfully', 'result': marshal(result, Auction_fields)}, 200
                else:
                    return {'message': 'Same as Before'}, 500
            else:
                return {'message': "You're not Seller" }, 501
        
        @jwt_required()
        @auc_ns.doc(
            description='경매 삭제하기.',
            responses={
                401: 'Invalid token',
                400: 'Missing Authorization header',
                200: 'Success',
                500: 'Same as Before',
                501: "You're not Seller"
            })
        @auth_ns.doc(security='Bearer')
        def delete(self, auctionid):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            if auctionService.select_is_seller(id, auctionid):
                result = auctionService.delete_auction(auctionid)
                if result:
                    return {'message': 'Auction delete successfully', 'result': marshal(result, Auction_fields)}, 200
                else:
                    return {'message': 'Same as Before'}, 500
            else:
                return {'message': "You're not Seller" }, 501

        @jwt_required()
        @auc_ns.doc(
            description='경매 조기 낙찰하기.',
            responses={
                401: 'Invalid token',
                400: 'Missing Authorization header',
                200: 'Success',
                500: 'Cannot Success Bid, need to find buyerid',
                501: "You're not Seller"
            })
        @auth_ns.doc(security='Bearer')
        def patch(self, auctionid):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            if auctionService.select_is_seller(id, auctionid):
                result = auctionService.complete_auction(auctionid)
                if result:
                    return {'message': 'Auction updated successfully', 'result': marshal(result, Bidded_fields)}, 200
                else:
                    return {'message': 'Cannot Success Bid, need to find buyerid'}, 500
            else:
                return {'message': "You're not Seller" }, 501
    
    @auc_ns.route('/<int:auctionid>/<int:price>')
    class AuctionbyOneWprice(Resource):
        @jwt_required()
        @auc_ns.doc(
            description='경매 금액 올리기',
            responses={
                401: 'Invalid token',
                400: 'Missing Authorization header',
                200: 'Success',
                500: 'Cannot Success Bid, need to find buyerid',
                501: "You're not Seller"
            })
        @auth_ns.doc(security='Bearer')
        def patch(self, auctionid, price):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            print(auctionService.select_is_seller(id=id, auctionid=auctionid))
            if not auctionService.select_is_seller(id=id, auctionid=auctionid):
                if AuctionService().countupAuctionPrice(auctionid, price, id):
                    return {'message': 'Auction updated successfully', 'result': f"{price}로 성공적으로 입찰하였습니다."}, 200
                else:
                    return {'message': f"{price}로 입찰실패하였습니다."}, 500
            else:
                return {'message': "You're not Buyer" }, 501    