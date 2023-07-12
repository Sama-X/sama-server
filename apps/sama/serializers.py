
from typing import Optional
from pydantic import BaseModel


class SamaNode(BaseModel):
    """
    SamaNodes
    """
    id: int
    work_key: str
    country: str
    local_ip: str
    public_ip: str
    min_port: int
    max_port: int
    check_port: int
    current_active_connect: int
    staker_type: Optional[int]
    staker_addr: Optional[str]
    work_addr: Optional[str]
    is_active: bool
    audit_node_info: Optional[int]
    cpu_info: Optional[int]
    memory_info: Optional[int]

    class Config:
        """
        Config.
        """
        orm_mode = True
