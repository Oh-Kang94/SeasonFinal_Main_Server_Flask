from datetime import datetime
from ..config.Config import db


def current_datetime():
    return datetime.utcnow()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(45), primary_key=True)
    password = db.Column(db.String(45))
    name = db.Column(db.String(45), nullable=True)
    nickname = db.Column(db.String(45), nullable=True)
    phone = db.Column(db.String(45), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    bankaccount = db.Column(db.String(45), nullable=True)
    insertdate = db.Column(db.DateTime, default=current_datetime())
    deletedate = db.Column(db.DateTime, default=None)
    refreshToken = db.Column(db.String(45), default=None)
    canseller = db.Column(db.Boolean, default=False)


class Balance(db.Model):
    __tablename__ = 'balance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(45), db.ForeignKey('user.id'))
    amount = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=current_datetime())

    # 관계성 만들기
    user = db.relationship('User', backref='Balance')


class Auction(db.Model):
    __tablename__ = 'auction'
    auctionid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(
        db.String(45), db.ForeignKey('user.id'), nullable=True)
    title = db.Column(db.String(45), nullable=True)
    content = db.Column(db.Text, nullable=True)
    pic = db.Column(db.String(45), nullable=True)
    fish = db.Column(db.String(45), nullable=True)
    view = db.Column(db.Integer, default = 0)
    pricestart = db.Column(db.Integer, nullable=True)
    pricenow = db.Column(db.Integer, nullable=True)
    insertdate = db.Column(db.DateTime, default=current_datetime())
    deletedate = db.Column(db.DateTime, nullable=True)
    issuccessed = db.Column(db.Boolean, default=False)
    # 관계성 만들기
    seller = db.relationship('User', backref='auctions')


class Bidded(db.Model):
    __tablename__ = 'bidded'
    biddedid = db.Column(db.Integer, primary_key=True)
    auctionid = db.Column(db.String(45), db.ForeignKey(
        'auction.auctionid'))
    buyerid = db.Column(db.String(45), db.ForeignKey('user.id'))
    biddedprice = db.Column(db.String(45), nullable=True)
    biddeddate = db.Column(db.String(45),  default=current_datetime())
    issuccessed = db.Column(db.Boolean, default=True)

    # 관계성 만들기
    auction = db.relationship('Auction', backref='bids')
    user = db.relationship('User', backref='bidded_items')

