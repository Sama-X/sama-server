"""
Sama service.
"""
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from sama import serializers
from sama.models import (
    SamaNode, SamaUser, SamaUserLog, UploadAuditNodeLog, UploadConnectLog,
    UploadNodeInfoLog
)

from base.response import APIResponse


async def get_sama_nodes(db: Session, country: str | None, page: int = 1, limit: int = 20):
    """
    Get sama nodes.
    """
    base = db.query(SamaNode).filter(SamaNode.is_active.is_(True), SamaNode.is_delete.is_(False))
    if country:
        base = base.filter(SamaNode.country == country)

    total = base.with_entities(
        func.COUNT(SamaNode.id)
    ).scalar()
    items = base.offset((page - 1) * limit).limit(limit).all()

    return total, items

async def upload_sama_config(db: Session, config: serializers.SamaNodeConfig):
    """
    Upload sama config.
    """
    with db.begin():
        node = db.query(SamaNode).filter(
            SamaNode.work_key == config.work_key,
            SamaNode.is_delete.is_(False)
        ).first()

        if node is None:
            return APIResponse(404, error="Node not found, plese check your work_key.")

        node.cpu_info = config.cpu_info
        node.memory_info = config.memory_info
        db.add(node)

        log = UploadNodeInfoLog(**{
            'work_key': config.work_key,
            'cpu_info': config.cpu_info,
            'memory_info': config.memory_info,
            'upload_time': datetime.now()
        })
        db.add(log)
        db.commit()

    return APIResponse(200)

async def upload_sama_audit(db: Session, config: serializers.SamaNodeAuditConfig):
    """
    Upload sama audit.
    """
    with db.begin():
        node = db.query(SamaNode).filter(
            SamaNode.work_key == config.work_key,
            SamaNode.is_delete.is_(False)
        ).first()

        if node is None:
            return APIResponse(404, error="Node not found, plese check your work_key.")

        node.audit_node_info = config.audit_node_info
        db.add(node)

        log = UploadAuditNodeLog(**{
            'work_key': config.work_key,
            'audit_node_info': config.audit_node_info,
            'upload_time': datetime.now()
        })
        db.add(log)
        db.commit()

    return APIResponse(200)


async def connect_sama_node(db: Session, config: serializers.SamaNodeConnectConfig):
    """
    Connect sama node.
    """
    with db.begin():
        node = db.query(SamaNode).filter(
            SamaNode.work_key == config.work_key,
            SamaNode.is_delete.is_(False)
        ).first()

        if node is None:
            return APIResponse(404, error="Node not found, plese check your work_key.")

        node.current_active_connect = config.active_connect_num
        db.add(node)
        log = UploadConnectLog(**{
            'work_key': config.work_key,
            'active_connect_num': config.active_connect_num,
            'upload_time': datetime.now()
        })
        db.add(log)
        db.commit()

    return APIResponse(200)


async def create_user(db: Session, user: serializers.UserCreate):
    """
    Create user.
    """
    with db.begin():
        obj = db.query(SamaUser).filter(
            SamaUser.address == user.address,
            SamaUser.is_delete.is_(False)
        ).first()

        log = SamaUserLog(**{
            'address': user.address,
            'start_time': user.start_time,
            'end_time': user.end_time,
            'upload_time': datetime.now()
        })
        db.add(log)

        if not obj:
            obj = SamaUser(**{
                'address': user.address,
                'start_time': user.start_time,
                'end_time': user.end_time,
            })
            db.add(obj)
        else:
            obj.start_time = user.start_time
            obj.end_time = user.end_time
            db.add(obj)

        db.commit()

        return APIResponse(200)
