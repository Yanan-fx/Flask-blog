from routes import db
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy.sql import func

class Comment(db.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=func.now())
    
    # 外键关联
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey('articles.id'), nullable=False)
    
    # 关系
    user = relationship("User", back_populates="comments")
    article = relationship("Article", back_populates="comments")
    
    def __repr__(self):
        return f"<Comment {self.id} by User {self.user_id} on Article {self.article_id}>" 