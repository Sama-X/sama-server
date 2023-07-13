"""
Sama API.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session

from sama import serializers, service

from base.models import get_db
from base.response import APIResponse


router = APIRouter(
    prefix="/api/v1/sama",
    tags=["sama"],
    dependencies=[],
    responses={404: {"error": "Not found"}},
)

@router.get("/nodes")
async def get_nodes(country: Annotated[str | None, Query(max_length=16)] = None,
                    page: Annotated[int, Query(ge=1)] = 1,
                    limit: Annotated[int, Query(ge=1)] = 20,
                    db: Session = Depends(get_db)):
    """
    Get all nodes.
    """
    total, items = await service.get_sama_nodes(db, country, page, limit)
    return APIResponse(
        200, data=[
            serializers.SamaNode.model_validate(
                item, from_attributes=True) for item in items
        ], total=total
    )


@router.post("/nodes/config")
async def upload_config(config: serializers.SamaNodeConfig,
                        db: Session = Depends(get_db)):
    """
    Upload config.
    """
    return await service.upload_sama_config(db, config)


@router.post("/nodes/audit")
async def upload_audit(config: serializers.SamaNodeAuditConfig,
                       db: Session = Depends(get_db)):
    """
    Upload audit.
    """
    return await service.upload_sama_audit(db, config)


@router.post("/nodes/connect")
async def upload_connect_node(config: serializers.SamaNodeConnectConfig,
                              db: Session = Depends(get_db)):
    """
    Connect node.
    """
    return await service.connect_sama_node(db, config)

@router.post("/users")
async def create_user(user: serializers.UserCreate,
                        db: Session = Depends(get_db)):
    """
    Create user.
    """
    return await service.create_user(db, user)
