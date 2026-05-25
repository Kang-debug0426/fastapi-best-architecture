from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column#导入DeclarativeBase、Mapped、mapped_column函数，用于创建ORM模型
from sqlalchemy import String, Integer,DateTime#
from datetime import datetime#导入datetime模块，用于处理日期和时间

class Base(DeclarativeBase):
    pass
class Note(Base):
    __tablename__ = "notes"#定义表名为notes
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)#定义id字段，类型为整数，是主键，并且自动递增
    title: Mapped[str] = mapped_column(String(100), nullable=False)#定义title字段，类型为字符串，最大长度为100，不能为空
    content: Mapped[str] = mapped_column(String(5000), nullable=False)#定义content字段，类型为字符串，最大长度为5000，不能为空
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)#定义created_at字段，类型为日期时间，默认值为当前UTC时间



   