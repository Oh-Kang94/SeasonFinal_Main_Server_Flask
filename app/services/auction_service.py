from app.services.user_service import UsersService
from ..models.DBModel import (
    Auction,
    Bidded
)
from ..config.Config import db
from ..util.util import current_datetime
from sqlalchemy.orm.exc import NoResultFound




class AuctionService:
    @staticmethod
    def create_auction(data, id):
        '''경매 열기 '''
        newAuction = Auction(
            seller_id=id,
            title=data['title'],
            content=data['content'],
            pic=data['pic'],
            fish=data['fish'],
            pricestart=data['pricestart']
        )
        db.session.add(newAuction)
        db.session.commit()
        return newAuction
    
    @staticmethod
    def select_all_auction():
        '''모든 경매 다 가져오기'''
        auctions = Auction.query.all()
        auctions_dict = [auction.as_dict() for auction in auctions]
        return auctions_dict

    @staticmethod
    def select_all_ongoing_auction():
        '''진행중인 경매 다 가져오기'''
        auctions = Auction.query.filter_by(
            deletedate=None, 
            issuccessed= False
            ).all()
        auctions_dict = [auction.as_dict() for auction in auctions]
        return auctions_dict

    @staticmethod
    def select_one_ongoing_auction(auctionid):
        '''진행중인 경매 하나 가져오기'''
        try:
            auction = Auction.query.filter_by(
                deletedate=None, issuccessed=False, auctionid=auctionid
            ).one()
        except NoResultFound:
            auction = None
        return auction

    @staticmethod
    def select_is_seller(id, auctionid):
        '''Seller가 맞는지 확인 여부'''
        result = Auction.query.filter_by(seller_id=id, auctionid=auctionid, deletedate=None, issuccessed=False).first()
        return result is not None

    @staticmethod
    def update_auction(data, id, auctionid):
        '''경매 수정하기 '''
        auction = Auction.query.filter_by(auctionid=auctionid, deletedate = None, issuccessed = False ).one()
        if auction:
            auction.title = data['title']
            auction.content = data['content']
            auction.pic = data['pic']
            auction.fish = data['fish']
            auction.endeddate = data['endeddate']
            auction.pricestart = data['pricestart']
            db.session.commit()
            return auction
        else:
            return None

    @staticmethod
    def delete_auction(auctionid):
        '''경매 취소하기'''
        auction = Auction.query.filter_by(auctionid=auctionid, deletedate = None, issuccessed = False ).one()
        if auction:
            auction.deletedate = current_datetime()
            db.session.commit()
            return auction
        else:
            return None
        
    @staticmethod
    def complete_auction(auctionid):
        '''경매 낙찰하기'''

        auction = Auction.query.filter_by(auctionid=auctionid).one()
        if auction:
            auction.issuccessed = True
            db.session.commit()
            try : 
                bidded = Bidded(
                    auctionid = auctionid,
                    buyerid = auction.buyer_id,
                    sellerid = auction.seller_id,
                    biddedprice = auction.pricenow,
                    biddeddate = current_datetime(),
                    address = UsersService.get_user_by_id(auction.buyer_id).address
                )
                db.session.add(bidded)
                db.session.commit()
                return bidded
            except:
                return None
        else:
            return None

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
            if auction.pricenow < price and auction.pricestart < price:
                auction.pricenow = price
                db.session.commit()
                auction.buyer_id = buyerid
                db.session.commit()
                return True
        else:
            return False
    
    @staticmethod
    def setCloseAuction(auctionid):
        '''시간 되면 경매 종료'''
        from app import app
        
        with app.app_context():
            auction = Auction.query.filter_by(auctionid=auctionid).first()
            if auction.buyer_id:
                auction.issuccessed = True
                db.session.commit()
                try : 
                    bidded = AuctionService.complete_auction(auctionid)
                    print(f"{auction.auctionid} 경매 완료!!")
                    return bidded
                except:
                    return None
            else:
                auction.issuccessed = False
                db.session.commit()
                f"{auction.auctionid} 경매 완료!!"
                return auction