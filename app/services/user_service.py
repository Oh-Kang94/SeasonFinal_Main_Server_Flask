from ..models.DBModel import User
from ..config.Config import db
class UsersService:
    @staticmethod
    def create_user(data):
        new_user = User(
            id=data['id'],
            password=data['password'],
            name=data['name'],
            nickname=data['nickname'],
            phone=data['phone'],
            address=data['address'],
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_user_by_id(id):
        return User.query.filter_by(id=id).first()
    
    @staticmethod
    def get_user_by_nickname(nickname):
        return User.query.filter_by(nickname=nickname).first()
    
    @staticmethod
    def get_nickname_by_id(id):
        return User.query.filter_by(id=id).first().nickname
    
    @staticmethod
    def update_nickname(id, new_nickname):
        # 이메일을 기반으로 사용자를 찾습니다.
        user = User.query.filter_by(id=id).first()

        if user:
            # 사용자가 존재하면 닉네임을 업데이트하고 저장합니다.
            user.nickname = new_nickname
            db.session.commit()
            return True
        else:
            return False
        
    @staticmethod
    def update_password(id, password, new_password):
        user = User.query.filter_by(id = id).first()

        if user:
            if user.password == password:
                user.password = new_password
                db.session.commit()
                return True
            else:
                return False
        else:
            return False