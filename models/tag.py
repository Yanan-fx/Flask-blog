from routes import db
from sqlalchemy import Integer, String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

# 文章与标签的多对多关联表
article_tags = Table(
    'article_tags',
    db.metadata,
    Column('article_id', Integer, ForeignKey('articles.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # 与文章的多对多关系
    articles = relationship("Article", secondary=article_tags, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag {self.name}>" 