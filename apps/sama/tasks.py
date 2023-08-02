"""
Sama tasks.
"""

import logging

from sqlalchemy.orm import Session

from fastapi import Depends
from celery import shared_task

from sama import serializers
from sama.models import SamaNode

from base.models import get_db
from base.sdk.dfx import DFXClient
from base.sdk.sama import SamaSDK


logger = logging.getLogger(__name__)


@shared_task
def get_sama_nodes(db = Depends(get_db)):
    """
    Get sama nodes.
    """
    logger.info("【get sama nodes】start")
    nodes = SamaSDK.get_sama_nodes()
    session: Session = next(db.dependency())
    if not session:
        logger.info("【get sama nodes】error reason: session is not exist")
        return

    with session.begin():
        db_nodes = session.query(SamaNode).filter(
            SamaNode.is_active.is_(True), SamaNode.is_delete.is_(False)
        ).with_entities(SamaNode.id, SamaNode.work_key).all()
        old_nodes = {item.work_key: item.id for item in db_nodes}
        new_nodes, delete_nodes = [], []
        for node in nodes:
            if node.workKey in old_nodes:
                old_nodes.pop(node.workKey)
            else:
                new_nodes.append(node)
        if old_nodes:
            delete_nodes = list(old_nodes.values())
            session.query(SamaNode).filter(SamaNode.id.in_(delete_nodes)).update(
                {
                    'is_active': False,
                    'is_delete': True
                },
                synchronize_session=False
            )
        if new_nodes:
            new_nodes = [
                {
                    'staker_type': node.stakerType,
                    'staker_addr': node.stakerAddr,
                    'country': node.country,
                    'work_key': node.workKey,
                    'local_ip': node.localIP,
                    'min_port': node.minPort,
                    'max_port': node.maxPort,
                    'public_ip': node.publicIP,
                    'check_port': node.checkPort,
                    'work_addr': node.workAddr,
                    'is_active': node.isActive,
                    'is_delete': False
                } for node in new_nodes
            ]
            session.bulk_insert_mappings(SamaNode, new_nodes)
        session.commit()

    logger.info(
        "【get sama nodes】end new_nodes: %s, delete_nodes: %s",
        len(new_nodes), len(delete_nodes)
    )


@shared_task
def upload_node_to_icp(work_key, db = Depends(get_db)):
    """
    Upload node to icp.
    """
    session: Session = next(db.dependency())
    if not session:
        logger.error("【upload node to icp】error reason: session is not exist")
        return
    logger.info("【upload node to icp】start")
    db_node = session.query(SamaNode).filter(
        SamaNode.is_active.is_(True), SamaNode.is_delete.is_(False),
        SamaNode.work_key == work_key
    ).first()
    if not db_node:
        logger.error("【upload node to icp】error reason: node is not exist")
        return
    item = serializers.SamaNode.model_validate(db_node, from_attributes=True)

    if DFXClient.get(work_key).data:
        result = DFXClient.update(work_key, item.model_dump_json())
    else:
        result = DFXClient.add(work_key, item.model_dump_json())

    logger.info("【upload node to icp】end upload result: %s", result.data)
