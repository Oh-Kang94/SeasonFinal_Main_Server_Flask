from flask_restx import Namespace


from ..routes.user_routes import user_routes
from ..routes.auction_routes import auction_routes
from ..routes.ai_routes import ai_routes
from ..routes.auth_routes import auth_routes
from ..routes.bidded_routes import bidded_routes
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

def register_namespaces(api):
    user_ns = Namespace("users", description= '유저 관련 정보')
    auth_ns = Namespace("auth", authorizations= authorizations, description="로그인 및 인증 관련")
    ai_ns = Namespace("ai", description= 'AI MODEL TEST용')
    auc_ns = Namespace("auctions", description= '경매 관련')
    bid_ns = Namespace("bidded", description= '경매결과 관련')

    user_routes(user_ns, auth_ns)
    auth_routes(auth_ns)
    ai_routes(ai_ns)
    auction_routes(auc_ns, auth_ns)
    bidded_routes(bid_ns, auth_ns)

    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(ai_ns)
    api.add_namespace(auc_ns)
    api.add_namespace(bid_ns)
