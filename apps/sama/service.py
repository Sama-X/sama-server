"""
Sama service.
"""
from sqlalchemy import func
from sqlalchemy.orm import Session

from sama.models import SamaNode


async def get_sama_nodes(db: Session, country: str | None, page: int = 1, limit: int = 20):
    """
    Get sama nodes.
    """
    base = db.query(SamaNode)
    if country:
        base = base.filter(SamaNode.country == country)

    total = base.with_entities(
        func.COUNT(SamaNode.id)
    ).scalar()
    items = base.offset((page - 1) * limit).limit(limit).all()

    return total, items
