
# -*- coding: utf-8 -*-
"""
角色表crud操作
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.api.apiV1.router.auth.schemas import RoleCreate,RoleUpdate
from app.api.common.curdBase import CRUDBase
from app.api.models.auth import AdminRole


class CRUDRole(CRUDBase[AdminRole, RoleCreate, RoleUpdate]):

    @staticmethod
    def query_role(db: Session, *, role_id: int) -> Optional[AdminRole]:
        """
        此role_id是否存在
        :param db:
        :param role_id:
        :return:
        """
        return db.query(AdminRole).filter(AdminRole.role_id == role_id).first()

    def create(self, db: Session, *, obj_in: RoleCreate) -> AdminRole:
        db_obj = AdminRole(
            role_id=obj_in.role_id,
            role_name=obj_in.role_name,
            permission_id=obj_in.permission_id,
            re_mark=obj_in.re_mark
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


curd_role = CRUDRole(AdminRole)
