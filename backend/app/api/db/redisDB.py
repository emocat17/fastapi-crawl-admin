#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通过class 实例化对象可以直接修改内部属性的特性
再通过魔法方法，赋予实例化对象 具有内部属性_redis_client的方法和属性

主要参考 flask-redis扩展实现
https://github.com/underyx/flask-redis/blob/master/flask_redis/client.py

redis 连接

"""
import sys

# 【修改1】: 导入 redis.asyncio 而不是 aioredis 的 create_redis_pool
# from aioredis import create_redis_pool, Redis # 旧的导入
import redis.asyncio as aioredis # 新的导入，使用 redis.asyncio 作为 aioredis 的替代
# from redis import Redis, AuthenticationError # 这个是同步 redis 库，保留用于 RedisCli
from redis import AuthenticationError # 同步 Redis 的 AuthenticationError
from redis import Redis as SyncRedis # 【可选修改】给同步 Redis 一个别名以区分

from app.api.logger import logger
from app.config import settings # 假设 settings.REDIS_URI, settings.REDIS_PASSWORD 等已定义

class RedisCli(object):
    """
    这个类看起来是用于同步 Redis 操作的。
    如果你的应用主要是异步的 (FastAPI 通常是)，
    你可能也想为这个类提供一个异步版本，或者确保只在同步上下文中使用它。
    """
    def __init__(self, *, host: str, port: int, password: str, db: int, socket_timeout: int = 5):
        self._redis_client: SyncRedis = None # 【可选修改】明确类型为同步 Redis
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.socket_timeout = socket_timeout

    def init_redis_connect(self) -> None:
        try:
            # 【可选修改】使用别名 SyncRedis
            self._redis_client = SyncRedis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                socket_timeout=self.socket_timeout, # 使用传入的 socket_timeout
                decode_responses=True
            )
            if not self._redis_client.ping():
                logger.info("连接redis超时")
                sys.exit() # 在库代码中直接 sys.exit() 可能不太好，最好抛出异常让调用者处理
        except AuthenticationError as e:
            logger.error(f"连接redis认证失败: {e}") # 使用 error 级别日志
            sys.exit()
        except Exception as e:
            logger.error(f"连接redis异常: {e}")
            sys.exit()

    def __getattr__(self, name):
        if self._redis_client is None:
            # 如果在未初始化时尝试访问属性，可以抛出错误或尝试初始化
            # self.init_redis_connect() # 或者更好的方式是在使用前确保已调用 init_redis_connect
            raise AttributeError(f"Redis client not initialized. Call init_redis_connect() first. Tried to access: {name}")
        return getattr(self._redis_client, name)

    # __getitem__, __setitem__, __delitem__ 对于现代 redis-py 可能不是必需的，
    # 因为主要通过方法调用 (get, set, delete) 而不是字典式访问。
    # 但如果你的代码依赖它们，可以保留。
    def __getitem__(self, name):
        if self._redis_client is None:
            raise AttributeError("Redis client not initialized.")
        return self._redis_client[name] # 这依赖于 redis-py 的旧行为或特定配置

    def __setitem__(self, name, value):
        if self._redis_client is None:
            raise AttributeError("Redis client not initialized.")
        self._redis_client[name] = value

    def __delitem__(self, name):
        if self._redis_client is None:
            raise AttributeError("Redis client not initialized.")
        del self._redis_client[name]


class RedisCore():
    """
    这个类用于异步 Redis 操作。
    """
    def __init__(self):
        # 你可以在这里初始化 redis 客户端，或者在每个需要它的方法中创建/获取
        # 为了示例清晰，我们将在 get_redis_client 方法中创建
        self._async_redis_client = None

    async def get_redis_client(self) -> aioredis.Redis: # 返回类型是 redis.asyncio.Redis
        """
        获取或创建异步 Redis 客户端实例。
        这个实例内部管理连接池。
        """
        if self._async_redis_client is None:
            # 【修改2】: 使用 aioredis.from_url (即 redis.asyncio.from_url)
            # settings.REDIS_URI 应该是类似 "redis://localhost:6379" 或 "redis://:password@localhost:6379/0"
            # from_url 会处理 URI 中的密码和数据库编号
            # 如果 settings.REDIS_URI 不包含密码或 db，而它们在单独的设置中，需要构造 URL
            # 假设 settings.REDIS_URI 已经包含了必要的信息
            # 或者，如果你的 settings.REDIS_URI 不包含密码和db，可以这样构造：
            # redis_url = f"redis://{':' + settings.REDIS_PASSWORD + '@' if settings.REDIS_PASSWORD else ''}{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DATABASE}"

            # 确保 settings.REDIS_URI 是完整的，或者按需构建
            # 示例：如果 settings.REDIS_URI 是 "redis://localhost:6379"
            # 而密码和db在 settings.REDIS_PASSWORD 和 settings.REDIS_DATABASE
            # 那么应该使用 redis.asyncio.Redis() 构造函数：
            # self._async_redis_client = aioredis.Redis(
            #     host=settings.REDIS_HOST,
            #     port=settings.REDIS_PORT,
            #     db=settings.REDIS_DATABASE,
            #     password=settings.REDIS_PASSWORD,
            #     encoding=settings.get("REDIS_ENCODING", "utf-8"), # 确保有默认值
            #     decode_responses=True # 通常在异步客户端中也设置为 True 以获取字符串
            # )
            # 或者，如果 settings.REDIS_URI 是完整的 "redis://[:password@]host:port/db"
            self._async_redis_client = aioredis.from_url(
                settings.REDIS_URI, # 确保这个 URI 是正确的
                encoding=getattr(settings, "REDIS_ENCODING", "utf-8"), # 使用 getattr 获取可选设置
                decode_responses=True # 推荐，除非你需要原始字节
            )
            logger.info(f"Async Redis client created for URI: {settings.REDIS_URI}")
        return self._async_redis_client

    async def close_redis_client(self):
        """
        关闭异步 Redis 客户端和其连接池。
        应该在应用关闭时调用。
        """
        if self._async_redis_client:
            await self._async_redis_client.close()
            # await self._async_redis_client.wait_closed() # 在 redis-py 4.x 中，close() 通常是足够的
            self._async_redis_client = None
            logger.info("Async Redis client closed.")

    # async def get_redis_info(self) -> dict: # 示例方法，现在使用 get_redis_client
    #     redis_connection = await self.get_redis_client() # 获取客户端实例
    #     info_item = {}
    #     # 【修改3】: 调用 info() 方法，它返回一个字典
    #     redis_info = await redis_connection.info() # info() 是一个异步方法
    #     # print(redis_info) # for debugging
    #     info_item['redis_version'] = redis_info.get('redis_version')
    #     info_item['os'] = redis_info.get('os')
    #     info_item['tcp_port'] = redis_info.get('tcp_port')
    #     info_item['used_memory_human'] = redis_info.get('used_memory_human')
    #     info_item['used_memory_peak_human'] = redis_info.get('used_memory_peak_human')
    #     return info_item

# 示例：如何使用 RedisCore (例如在 FastAPI 的 startup/shutdown 事件中)
# redis_core_manager = RedisCore()

# @app.on_event("startup")
# async def startup_event():
#     # 初始化同步 Redis (如果需要)
#     # redis_client.init_redis_connect()

#     # 初始化异步 Redis 客户端 (get_redis_client 会在首次调用时创建)
#     # 你也可以在这里显式调用一次以确保连接（尽管 from_url 通常是惰性的）
#     await redis_core_manager.get_redis_client()
#     logger.info("Async Redis client is ready.")

# @app.on_event("shutdown")
# async def shutdown_event():
#     # 关闭异步 Redis 客户端
#     await redis_core_manager.close_redis_client()

#     # 同步 redis_client (RedisCli) 没有显式的 close 方法，
#     # 连接通常由 redis-py 库在对象被垃圾回收时处理，或者依赖于连接池。
#     # 对于长时间运行的应用，显式关闭或使用连接池更好。