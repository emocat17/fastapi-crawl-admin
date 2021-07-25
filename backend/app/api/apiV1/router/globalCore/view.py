# -*- coding: utf-8 -*
# @Time : 2020/11/10 15:00
import psutil
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.api.db.redisCurd import RedisQueue
from app.api.db.session import get_db
from app.api.models.hosts import Hosts
from app.api.models.proTask import Project, Tasks
from app.api.utils.responseCode import resp_200, resp_500

router = APIRouter()


# 总项目数量/总任务数量
def globalCount(*, request: Request, db: Session = Depends(get_db),
                # token_data: Union[str, Any] = Depends(deps.check_jwt_token)
                ):
    item = {}
    item["projectCount"] = db.query(Project).count()
    item["taskCount"] = db.query(Tasks).count()
    item["hostCount"] = db.query(Hosts).count()
    return resp_200(data=item)

# 系统信息
def systemParams(
        *, request: Request
):
    try:
        result = [
            {'title': '内存信息', 'total': psutil.virtual_memory().total, 'free': psutil.virtual_memory().free,
             'percent': int((psutil.virtual_memory().free / psutil.virtual_memory().total) * 100)},
            {'title': 'CPU信息', 'total': psutil.cpu_times().system, 'free': psutil.cpu_times().user},
        ]
        return resp_200(data=result)
    except:
        return resp_500()


# redis参数
def redisParam(
        *, request: Request,
        # token_data: Union[str, Any] = Depends(deps.check_jwt_token)
):
    info = RedisQueue().info()
    print(info)
    return resp_200(data=info)

# redis参数
def mysqlParam(
        *, request: Request,
        db: Session = Depends(get_db),
        # token_data: Union[str, Any] = Depends(deps.check_jwt_token)
):
    info = RedisQueue().info()
    print(info)
    return resp_200(data=info)


# ------------------------------- 路由添加 --------------------------------

router.add_api_route(methods=['GET'], path="/global/count",endpoint=globalCount, summary="全局统计")
router.add_api_route(methods=['GET'], path="/global/sys", endpoint=systemParams,summary="系统信息")
router.add_api_route(methods=['GET'], path="/global/redis",endpoint=redisParam, summary="redis参数")
router.add_api_route(methods=['GET'], path="/global/mysql",endpoint=mysqlParam, summary="mysql参数")
