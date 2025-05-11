from routes import db
from sqlalchemy import Integer, String, BLOB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime
from sqlalchemy.sql import func
from models.tag import article_tags

class Article(db.Model):
    __tablename__ = 'articles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    __content: Mapped[bytes] = mapped_column(BLOB, name="content", nullable=True)
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=func.now())
    update_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True, default=func.now(), onupdate=func.now())
    
    # 与标签的多对多关系
    tags = relationship("Tag", secondary=article_tags, back_populates="articles")
    
    # 与评论的一对多关系
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")

    @property
    def content(self):
        return self.__content.decode('utf-8')

    @content.setter #用来添加content数据
    def content(self, value):
        if isinstance(value, str):
            self.__content = value.encode('utf-8')
        else:
            self.__content = value
            
    def get_tags_string(self):
        """返回标签的字符串表示，逗号分隔"""
        return ', '.join([tag.name for tag in self.tags])