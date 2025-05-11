from routes import db
from sqlalchemy import Integer, String, BLOB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.sql import func

class Article(db.Model):
    __tablename__ = 'articles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    __content: Mapped[bytes] = mapped_column(BLOB, name="content", nullable=True)
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=func.now())
    update_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True, default=func.now(), onupdate=func.now())

    @property
    def content(self):
        return self.__content.decode('utf-8')

    @content.setter #用来添加content数据
    def content(self, value):
        if isinstance(value, str):
            self.__content = value.encode('utf-8')
        else:
            self.__content = value