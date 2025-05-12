from sqlalchemy import Select
from models.tag import Tag
from routes import db

class TagService:
    def get_all_tags(self):
        """获取所有标签"""
        query = Select(Tag)
        return db.session.scalars(query).all()
        
    def get_tag_by_name(self, name):
        """根据名称获取标签"""
        query = Select(Tag).where(Tag.name == name)
        return db.session.scalar(query)
        
    def get_or_create_tag(self, name):
        """获取标签，如果不存在则创建"""
        # 标准化标签名称：去除首尾空格，转为小写
        name = name.strip().lower()
        if not name:
            return None
            
        # 尝试获取现有标签
        tag = self.get_tag_by_name(name)
        
        # 如果不存在，则创建
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()
            
        return tag
        
    def get_or_create_tags(self, tags_string):
        """从逗号分隔的标签字符串创建多个标签"""
        if not tags_string:
            return []
            
        # 分割标签字符串
        tag_names = [name.strip().lower() for name in tags_string.split(',') if name.strip()]
        tags = []
        
        for name in tag_names:
            tag = self.get_or_create_tag(name)
            if tag:
                tags.append(tag)
                
        return tags 