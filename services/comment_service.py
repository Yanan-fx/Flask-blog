from models.comment import Comment
from routes import db
from sqlalchemy import Select, desc
from typing import List, Optional

class CommentService:
    def get_comments_by_article(self, article_id: int) -> List[Comment]:
        """获取指定文章的所有评论，按时间倒序排列"""
        query = Select(Comment).where(Comment.article_id == article_id).order_by(desc(Comment.create_time))
        return db.session.scalars(query).all()
    
    def get_comment(self, comment_id: int) -> Optional[Comment]:
        """获取指定评论"""
        return db.session.get(Comment, comment_id)
    
    def create_comment(self, comment: Comment) -> Comment:
        """创建评论"""
        db.session.add(comment)
        db.session.commit()
        return comment
    
    def delete_comment(self, comment_id: int) -> bool:
        """删除评论"""
        comment = self.get_comment(comment_id)
        if not comment:
            return False
        
        db.session.delete(comment)
        db.session.commit()
        return True
    
    def can_delete_comment(self, comment_id: int, user_id: int, is_admin: bool) -> bool:
        """检查用户是否可以删除评论（自己的评论或管理员）"""
        comment = self.get_comment(comment_id)
        if not comment:
            return False
        
        # 管理员可以删除任何评论
        if is_admin:
            return True
        
        # 用户只能删除自己的评论
        return comment.user_id == user_id 