from sqlalchemy import desc, or_
from ..models.DBModel import (
    Auction,
    Bidded
)
from ..config.Config import db
from ..util.util import current_datetime

class BiddedService:
    @staticmethod
    def select_auction_all():
        '''경매결과 다 가져오기 - "경매완료일 내림차순"'''
        biddeds = Bidded.query.filter_by(
            deletedate=None, 
            issuccessed= False
            ).order_by(desc(Bidded.biddeddate)).all()
        bidded_list = [bidded.as_dict() for bidded in biddeds]
        return bidded_list
    
    @staticmethod
    def select_auction_query(query , value):
        '''경매결과 쿼리로 찾기"'''
        biddeds = Bidded.query.filter(getattr(Bidded, query) == value).all()
        # 이 경우 하나의 조건만 사용합니다.
        # getattr() 함수를 사용하여 Bidded 클래스의 속성을 동적으로 가져옵니다.
        # query 변수에 저장된 문자열 값이 Bidded 클래스의 속성과 일치하는지 확인합니다.
        bidded_list = [bidded.as_dict() for bidded in biddeds]
        return bidded_list
    