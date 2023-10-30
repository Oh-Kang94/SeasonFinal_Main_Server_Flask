from flask_restx import Namespace


from ..routes.user_routes import user_routes
from ..routes.auction_routes import auction_routes
from ..routes.ai_routes import ai_routes
from ..routes.auth_routes import auth_routes
from ..routes.bidded_routes import bidded_routes
from ..routes.balance_routes import balance_routes
from ..routes.sched_routes import sched_routes
from apscheduler.schedulers.background import BackgroundScheduler
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

def register_namespaces(api):
    user_ns = Namespace("users", description= '유저 관련 정보')
    auth_ns = Namespace("auth", authorizations= authorizations, description="로그인 및 인증 관련")
    ai_ns = Namespace("ai", description= 'AI MODEL TEST용')
    auc_ns = Namespace("auctions", description= '경매 관련')
    bid_ns = Namespace("bidded", description= '경매결과 관련')
    bal_ns = Namespace("balance", description= '유저의 포인트')
    sched_ns = Namespace("sched", description= '스케쥴 전용 (사용금지)')

    user_routes(user_ns, auth_ns)
    auth_routes(auth_ns)
    ai_routes(ai_ns)
    auction_routes(auc_ns, auth_ns)
    bidded_routes(bid_ns, auth_ns)
    balance_routes(bal_ns, auth_ns)
    from app import redis_client
    sched_routes(sched_ns, redis_client)

    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(ai_ns)
    api.add_namespace(auc_ns)
    api.add_namespace(bid_ns)
    api.add_namespace(bal_ns)
    api.add_namespace(sched_ns)

    scheduler = BackgroundScheduler()
    scheduler.add_job(sched_routes, 'cron', args=[sched_ns, redis_client], hour=9, minute=40)
    scheduler.start()


