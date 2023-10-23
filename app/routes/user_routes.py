from flask_restx import Resource, fields
from ..services.auth_service import AuthService
from flask import request
from ..config.Config import api
from ..services.user_service import UsersService
from flask_jwt_extended import jwt_required


def user_routes(user_ns, auth_ns):

    authService = AuthService()

    @user_ns.route('/registration')
    class Register(Resource):
        @user_ns.doc(
            description='회원가입',
            responses={
                400: 'User already exists',
                200: 'User created successfully',
            })
        @user_ns.expect(api.model('Register', {
            'id': fields.String(description='ID로 쓰임', example='okh19941994@naver.com'),
            'password': fields.String(description='비밀번호', example='qwer1234'),
            'name': fields.String(description='사용자 이름', example='오강현'),
            'nickname': fields.String(description='사용자 닉네임', example='Oh-Kang94'),
            'phone': fields.String(description='사용자 전화번호', example='010-1234-5678'),
            'address': fields.String(description='사용자 주소', example='서울시 동대문구'),
        }))
        def post(self):
            data = api.payload
            id = data['id']
            if UsersService.get_user_by_id(id):
                return {'message': 'User already exists'}, 400

            new_user = UsersService.create_user(data)
            return {'message': 'User created successfully', 'id': new_user.id}, 200

    @user_ns.route('/id/<string:id>')
    class findEmail(Resource):
        @user_ns.doc(
            description='아이디 중복 확인',
            responses={
                400: 'Email Duplicated',
                200: 'Success',
            })
        def get(self, id):
            if UsersService.get_user_by_id(id):
                return {'message': 'Email Duplicated'}, 400
            return {'message': 'Success'}, 200

    @user_ns.route('/nickname/<string:nickname>')
    class findNickname(Resource):
        @user_ns.doc(
            description='닉네임 중복 확인',
            responses={
                403: 'Nickname Duplicated',
                200: 'Success',
            })
        def get(self, nickname):
            if UsersService.get_user_by_nickname(nickname):
                return {'message': 'Nickname Duplicated'}, 400
            return {'message': 'Success'}, 200

        @jwt_required()
        @auth_ns.doc(security='Bearer')
        @user_ns.doc(
            description='닉네임 변경',
            responses={
                200: 'Nickname updated successfully',
                300: 'Server Error',
                400: 'Missing Authorization header',
                401: 'Invalid token',
                403: 'Nickname Duplicated',
            })
        @user_ns.expect()
        def put(self, nickname):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            user_id = auth_result
            if UsersService.get_user_by_nickname(nickname):
                return {'message': 'Nickname Duplicated'}, 403
            if UsersService.update_nickname(user_id, nickname):
                return {'message': 'Nickname updated successfully'}, 200
            else:
                return {'message': 'Server Error'}, 300

    @user_ns.route('/password')
    class changePassword(Resource):
        @user_ns.doc(
            description='패스워드 변경',
            responses={
                401: 'Invalid token',
                400: 'Missing Authorization header',
                200: 'User updated successfully',
                403: 'Wrong Password'
            })
        @user_ns.expect(api.model('Password', {
            'current': fields.String(description='현재 비밀번호', example='asdjifnaisndfoiajsdfjaosdjfdsa'),
            'new': fields.String(description='새로운 비밀번호', example='dsjfnjklnfdjglsnlkfjiwesfidnfilss'),
        }))
        @jwt_required()
        @auth_ns.doc(security='Bearer')
        def put(self):
            authorization_header = request.headers.get('Authorization')
            auth_result = authService.authenticate_request(
                authorization_header)
            if isinstance(auth_result, dict):
                return auth_result
            user_id = auth_result
            data = api.payload
            currentPW = data['current']
            newPW = data['new']
            if UsersService.update_password(user_id, currentPW, newPW):
                return {'message': 'User updated successfully'}, 200
            else:
                return {'message': 'Wrong Password'}, 403
