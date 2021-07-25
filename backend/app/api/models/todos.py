# -*- coding: utf-8 -*
# @Time : 2020/11/10 13:37

import time

from sqlalchemy import Boolean, Column, DateTime, Integer, Text

from app.api.db.baseClass import Base


class Todos(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, comment='标题')
    status = Column(Boolean, comment='状态',default=0)
    update_time = Column(DateTime, default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), comment='更新时间')


