from ..models.DBModel import User
from ..config.Config import db
class UsersService:
    @staticmethod
    def create_user(data):
        ''' user 회원가입하기'''  
        if data['bankaccount'] is not None:
            new_user = User(
            id=data['id'],
            password=data['password'],
            name=data['name'],
            nickname=data['nickname'],
            bankaccount=data['bankaccount'],
            phone=data['phone'],
            address=data['address'],
            canseller = True
            )
            db.session.add(new_user)
            db.session.commit()
        else:
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
        '''user가 id로 있는지 체크'''
        return User.query.filter_by(id=id).first()
    
    @staticmethod
    def get_user_by_nickname(nickname):
        '''user가 nickname으로 있는지 체크'''
        return User.query.filter_by(nickname=nickname).first()
    
    @staticmethod
    def get_nickname_by_id(id):
        '''id로 nickname 검색하기'''
        return User.query.filter_by(id=id).first().nickname
    
    @staticmethod
    def update_nickname(id, new_nickname):
        '''nickname 변경하기'''
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
        '''비밀번호 바꾸기'''
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
    
    @staticmethod
    def select_user_all():
        '''유저 리스트 전부 가져오기'''
        users = User.query.all()
        users_list = [user.as_dict() for user in users]
        return users_list