from ..models.DBModel import Balance
from ..config.Config import db
from sqlalchemy import func

class BalanceService:
    @staticmethod
    def select_my_point(id):
        '''개인의 총 포인트 확인'''
        total_amount = db.session.query(func.sum(Balance.amount)).filter(Balance.userid == id).first()[0]
        print(total_amount)
        # - session.query(func.sum(User.amount)): User 모델의 amount 컬럼에 대해 합계를 계산하는 쿼리를 생성합니다.
        # - .filter(User.userid == your_userid): userid가 특정 값 (your_userid)과 일치하는 사용자들을 선택합니다.
        # - .scalar(): 결과를 단일 값으로 가져옵니다. 총 합계를 반환합니다.
        return total_amount
    
    @staticmethod
    def insert_point(amount, id):
        '''충전 및 환급내역 추가'''
        new_balance = Balance(
            userid = id,
            amount = amount
        )
        db.session.add(new_balance)
        db.session.commit()
        new_amount = BalanceService.select_my_point(id)
        return new_amount