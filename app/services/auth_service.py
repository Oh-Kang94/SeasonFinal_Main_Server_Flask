from flask_jwt_extended import decode_token
from ..config.Config import db
from ..models.DBModel import User

class AuthService:
    @staticmethod
    def decode_token(header):
        '''JWT 복호화 시키기 (header값 필요)'''
        try:
            # 'Bearer' 부분을 제외한 토큰만 추출
            token = header.split()[1]
            # 토큰 디코딩
            decoded_token = decode_token(token)
            return decoded_token
        except Exception as e:
            print(f"Error decoding token: {e}")
            return None
        
    @staticmethod
    def set_refreshtoken(id, refreshtoken):
        '''RefreshToken으로 id와 검증후, Access재발급'''
        user = User.query.filter_by(id=id).first()
        user.refreshtoken = refreshtoken
        db.session.commit()
        return True
    
    @staticmethod
    def authenticate_request(authorization_header):
        if authorization_header and authorization_header.startswith('Bearer '):
            decoded_token = AuthService.decode_token(authorization_header)
            if decoded_token:
                # 여기서 'sub'는 사용자의 이메일 주소를 의미합니다.
                id = decoded_token.get('sub')
                return id
            else:
                return {'message': 'Invalid token'}, 401
        else:
            return {'message': "Invalid or missing Authorization header"}, 400