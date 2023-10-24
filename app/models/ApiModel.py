from flask_restx import fields

from ..config.Config import api

from flask_restx import fields

User_fields = api.model('User', {
   'id': fields.String(required=True, description='User ID'),
   'password': fields.String(description='Password'),
   'name': fields.String(description='Name'),
   'nickname': fields.String(description='Nickname'),
   'phone': fields.String(description='Phone'),
   'address': fields.String(description='Address'),
   'bankaccount': fields.String(description='Bank Account'),
   'insertdate': fields.DateTime(description='Insert Date', dt_format="iso8601"),
   'deletedate':  fields.DateTime(description='Delete Date', dt_format="iso8601", required=False),
   'refreshtoken':  fields.String(description='Refresh Token', required=False),
   'canseller': fields.Boolean(description='Can Seller')
})

Balance_fields = api.model('Balance', {
   "id": fields.Integer(readOnly=True, description="Balance ID"),
   "userid": fields.String(required=True, description="User ID"),
   "amount": fields.Integer(required=True, description="Amount"),
   "date": fields.DateTime(required=True, description="Date", dt_format="iso8601")
})

Bidded_fields = api.model('Bidded', {
   "biddedid": fields.Integer(readOnly=True, description="Bidded ID"),
   "auctionid": fields.String(required=True, description="Auction ID"),
   "buyerid": fields.String(required=True, description="Buyer ID"),
   "biddedprice": fields.Float(required=True, description="Bidded Price"),
   "biddeddate": fields.DateTime(dt_format="iso8601", required=False),
})

Auction_fields = api.model('Auction', {
   "auctionid":fields.Integer(readOnly=True, description=" Auction Id "),
   "seller_id":fields.String(Required=True, description=" Seller Id "),
   "title":fields.String(Required=True, description=" Title "),
   "content":fields.String(Required=True, description=" Content "),
   "pic": fields.String(Required=False, nullable=True),
   "fish": fields.String(Required=False, nullable=True),
   "view": fields.Integer(),
   "pricestart":fields.Integer(),
   "pricenow":  fields.Integer(),
   'insertdate': fields.DateTime(format="iso8601", required=True),
   "deletedate":fields.DateTime(dt_format="iso8601", required=False),
   "issuccessed":fields.Boolean(default=False)
})

Login_fields = api.namespace('Auth').model('Auth', {
   'id': fields.String(required=True, example='okh19941994@naver.com'),
   'password': fields.String(required=True, example='qwer1234')
})
