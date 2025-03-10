from flask_session import Session
import redis
from .config import REDIS_SERVER_ADDRESS,SECRET_KEY  # 导入 Redis 服务器地址

def configure_redis_session(app):
    # 配置 session 使用 Redis
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url(REDIS_SERVER_ADDRESS)

    app.config['SECRET_KEY'] = SECRET_KEY
    # 初始化 Session
    Session(app)