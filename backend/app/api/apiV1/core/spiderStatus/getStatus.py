# -*- coding: utf-8 -*
# @Time : 2020/12/3 9:11
import time

from sqlalchemy.orm import Session

from app.api.db.session import get_db, SessionLocal
from app.api.models.proTask import Tasks

db: Session = SessionLocal()


def startSpiderStatus(taskId):
    taskInfo = db.query(Tasks).filter(Tasks.task_id == taskId).first()
    try:
        taskInfo.task_status = 0
        taskInfo.last_run_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db.commit()
        return {'status_code': 200, 'message': '状态更新成功'}
    except:
        print("产生数据库回滚 ！！！")
        db.rollback()


def endSpiderStatus(taskId, spiderStatus=1):
    taskInfo = db.query(Tasks).filter(Tasks.task_id == taskId).first()
    try:
        taskInfo.task_status = 1
        taskInfo.last_run_status = spiderStatus
        taskInfo.last_run_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db.commit()
        return {'status_code': 200, 'message': '状态更新成功'}
    except:
        print("产生数据库回滚 ！！！")
        db.rollback()


def getSpiderStatus(taskId):
    taskInfo = db.query(Tasks).filter(Tasks.task_id == taskId).first()
    try:
        return {'status_code': 200, 'message': '获取状态成功', 'data': taskInfo.task_status}
    except:
        print("产生数据库回滚 ！！！")
        db.rollback()
        return {'status_code': 306, 'message': 'ID不存在，我也帮不了你'}
