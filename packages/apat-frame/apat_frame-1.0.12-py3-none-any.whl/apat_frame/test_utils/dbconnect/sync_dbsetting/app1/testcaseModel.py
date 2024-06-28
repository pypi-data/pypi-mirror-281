from sqlalchemy import Column, Integer, String, Text, DateTime ,func
from sqlalchemy.orm import declarative_base  # 修改这里的导入方式

Base = declarative_base()

class CaseManageModel(Base):
    __tablename__ = 'casemanage'
    
    code = Column(String(255), primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    category1 = Column(String(50))
    category2 = Column(String(50), nullable=True)
    status = Column(Integer, nullable=True)
    script = Column(Text)
    expected = Column(Text)
    actual = Column(Text)
    result = Column(String(50), nullable=True)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, onupdate=func.now())
    creator = Column(String(50), nullable=True)
    updater = Column(String(50), nullable=True)

def model_to_dict(instance):
    """
    将SQLAlchemy模型实例转换为字典。
    
    参数:
    - instance: SQLAlchemy模型的实例
    
    返回:
    一个字典，其中键为模型属性名，值为属性值。
    """
    if instance is None:
        return {}
    return {c.key: getattr(instance, c.key) for c in instance.__table__.columns}