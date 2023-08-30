"""
SamaNode serializer.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator


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
    audit_node_info: Optional[str]
    cpu_info: Optional[str]
    memory_info: Optional[str]
    modified_time: Optional[str]

    class Config:
        """
        Config.
        """
        from_attributes = True


class SamaNodeConfig(BaseModel):
    """
    SamaNode config.
    """
    work_key: str
    cpu_info: Optional[str]
    memory_info: Optional[str]


class SamaNodeAuditConfig(BaseModel):
    """
    SamaNode audit config.
    """
    work_key: str
    audit_node_info: Optional[str]


class SamaNodeConnectConfig(BaseModel):
    """
    SamaNode connect config.
    """
    work_key: str
    active_connect_num: int


class UserCreate(BaseModel):
    """
    User create.
    """
    address: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]

    @validator("start_time", pre=True)
    def parse_start_time(cls, value):  # pylint: disable=E0213
        """
        Parse start time.
        """
        return datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S"
        ).date()

    @validator("end_time", pre=True)
    def parse_end_time(cls, value):  # pylint: disable=E0213
        """
        Parse end time.
        """
        return datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S"
        ).date()
