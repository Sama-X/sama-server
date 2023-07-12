"""
Sama models.
"""

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, Text
from base.models import Base, ModelBase, engine


class SamaNode(ModelBase, Base):
    """
    Sama node model.
    """
    STAKER_TYPE_AUDITOR = 6
    STAKER_TYPE_WORK = 7
    STAKER_TYPE_VALIDATOR = 18

    __tablename__ = "sama_node"

    work_key = Column(String(256), index=True, comment="工作密钥")
    country = Column(String(16), index=True, comment="国家")
    local_ip = Column(String(32), index=True, comment="内网IP")
    public_ip = Column(String(32), index=True, comment="公网IP")
    min_port = Column(Integer, comment="最小端口")
    max_port = Column(Integer, comment="最大端口")
    check_port = Column(Integer, comment="检查端口")
    current_active_connect = Column(Integer, default=0, comment="当前活跃连接数")
    staker_type = Column(SmallInteger, index=True, default=STAKER_TYPE_AUDITOR, comment="质押类型")
    staker_addr = Column(String(256), nullable=True, comment="质押地址")
    work_addr = Column(String(256), nullable=True, comment="工作地址")
    is_active = Column(SmallInteger, index=True, default=0, comment="是否激活")
    audit_node_info = Column(Text, nullable=True, comment="审核节点信息")
    cpu_info = Column(String(32), nullable=True, comment="CPU信息")
    memory_info = Column(String(32), nullable=True, comment="内存信息")


class SamaUser(ModelBase, Base):
    """
    Sama user model.
    """
    __tablename__ = "sama_user"

    address = Column(String(256), index=True, comment="钱包地址")
    start_time = Column(DateTime, nullable=True, comment="开始时间")
    end_time = Column(DateTime, nullable=True, comment="结束时间")


class UploadConnectLog(ModelBase, Base):
    """
    Upload connect log model.
    """
    __tablename__ = "upload_connect_log"

    work_key = Column(String(256), index=True, comment="工作密钥")
    active_connect_num = Column(Integer, comment="活跃连接数")
    upload_time = Column(DateTime, nullable=True, comment="上传时间")

class UploadAuditNodeLog(ModelBase, Base):
    """
    Upload audit node log model.
    """
    __tablename__ = "upload_audit_node_log"

    work_key = Column(String(256), index=True, comment="工作密钥")
    audit_node_info = Column(Text, nullable=True, comment="审核节点信息")
    upload_time = Column(DateTime, nullable=True, comment="上传时间")


class UploadNodeInfoLog(ModelBase, Base):
    """
    Upload node info log model.
    """
    __tablename__ = "upload_node_info_log"

    work_key = Column(String(256), index=True, comment="工作密钥")
    cpu_info = Column(String(32), nullable=True, comment="CPU信息")
    memory_info = Column(String(32), nullable=True, comment="内存信息")
    upload_time = Column(DateTime, nullable=True, comment="上传时间")


Base.metadata.create_all(bind=engine)
