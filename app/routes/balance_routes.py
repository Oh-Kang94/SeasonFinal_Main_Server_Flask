
from flask_restx import Resource, fields, marshal
from flask import request
from flask_jwt_extended import jwt_required
from app.services.balance_service import BalanceService
from app.services.auth_service import AuthService
from ..models.ApiModel import Balance_fields
from ..config.Config import api


def balance_routes(bal_ns, auth_ns):
    balanceService = BalanceService()
    authService = AuthService()

    @bal_ns.route("/")
    class BalanceForOne(Resource):
        @jwt_required()
        @bal_ns.doc(
            description='현 포인트 확인해 보기',
            responses={
                401: 'Invalid token',
                400: 'Missing Authorization header',
                200: 'Success',
                406: "You haven't use yet",
            })
        @auth_ns.doc(security='Bearer')
        def get(self):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            if id == 'root':
                result = balanceService.select_all_point()
                return {'message': 'All Balances Loaded Successfully', 'result': marshal(result, Balance_fields)}, 200
            else :
                result = balanceService.select_my_point(id)
                if result:
                    return {'message': 'Amounts Loaded Successfully', 'result': str(result)}, 200
                else:
                    return {'message': "You haven't use yet"}, 500

        @jwt_required()
        @bal_ns.doc(
            description='포인트 입금 출금하기(convert, charge)',
            responses={
                401: 'Invalid token',
                400: 'Missing Authorization header',
                200: 'Success',
                400: 'You should give right request',
                406: "Not enough have point",
            })
        @auth_ns.doc(security='Bearer')
        @bal_ns.expect(api.model('CreateBalance', {
            'method': fields.String(description='충전인지 환급인지(convert, charge)', example='charge'),
            'amount': fields.String(description='충전 및 환급 금액', example='10000'),
        }))
        def post(self):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            id = auth_result
            data = api.payload
            amount = int(data["amount"])
            balance = balanceService.select_my_point(id)
            if data['method'] == "convert":
                if balance - amount <= 0:
                    return {"result": "Not enough have point", "amount": str(balance)}, 406
                else:
                    new_balance = balanceService.insert_point(-amount, id)
                    return {"result": "Success", "Amount": str(new_balance)}, 200
            elif data['method'] == "charge":
                new_balance = balanceService.insert_point(amount, id)
                return {"result": "Success", "Amount": str(new_balance)}, 200
            else:
                return {"result": 'You should give right request'}, 400 
