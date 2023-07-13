"""
Sama service.
"""
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from sama import serializers
from sama.models import SamaNode, UploadAuditNodeLog, UploadNodeInfoLog

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
