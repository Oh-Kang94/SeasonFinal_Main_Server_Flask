from ..models.DBModel import (
    User,
    Auction
)
from ..config.Config import db

class AuctionService:
    @staticmethod
    def create_auction(data, id):
        '''경매 열기 '''
        newAuction = Auction(
            seller_id = id,
            title = data['title'],
            content = data['content'],
            pic = data['pic'],
            fish = data['fish'],
            pricestart = data['pricestart']
        )
        db.session.add(newAuction)
        db.session.commit()
        return newAuction
    
    @staticmethod
    def update_auction(data, id, auctionid):
        '''경매 수정하기 '''
        auctionid = Auction.query.filter_by(auctionid=auctionid).first()
        newAuction = Auction(
            seller_id = id,
            title = data['title'],
            content = data['content'],
            pic = data['pic'],
            fish = data['fish'],
            pricestart = data['pricestart']
        )
        db.session.add(newAuction)
        db.session.commit()
        return newAuction
    
    @staticmethod
    def update_password(id, password, new_password):
        user = User.query.filter_by(id=id).first()

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
    def countupAuctionView(auctionid):
        '''경매 들어가면 조회수 늘리기'''
        auction = Auction.query.filter_by(auctionid=auctionid).first()
        if auction:
            auction.view = int(auction.view) + 1
            db.session.commit()
            return True
        else:
            return False
        
    @staticmethod
    def countupAuctionPrice(auctionid, price, buyerid):
        '''경매 가격 Raise'''
        auction = Auction.query.filter_by(auctionid=auctionid).first()
        if auction:
            if auction.pricenow and auction.pricestart < price:
                auction.pricenow = price
                db.session.commit()
                return True
        else:
            return False
