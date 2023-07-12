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
