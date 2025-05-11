from models import article
from models.article import Article
from models.tag import Tag
from routes import db
from sqlalchemy import Select, func, and_, or_, text


class ArticleService:

    def get_article(self, id):
        return db.session.get(Article,id)

    def get_articles(self):
        query = Select(Article)
        return db.session.scalars(query).all()

    def get_articles_by_tag(self, tag_id):
        """获取指定标签的所有文章"""
        tag = db.session.get(Tag, tag_id)
        if tag:
            return tag.articles
        return []

    def search_articles(self, query_text):
        """搜索文章（标题、内容、标签）"""
        if not query_text:
            return []
            
        # 标准化搜索词，去除多余空格
        query_text = query_text.strip().lower()
        
        # ILIKE操作符用于不区分大小写的模糊匹配
        # 使用or_组合多个搜索条件
        articles_with_matching_title_or_content = db.session.query(Article).filter(
            or_(
                func.lower(Article.title).contains(query_text),
                # 对于内容，我们需要转换BLOB类型为字符串再搜索
                func.lower(Article._Article__content).cast(db.String).contains(query_text.encode('utf-8'))
            )
        ).all()
        
        # 搜索匹配标签的文章
        matching_tags = db.session.query(Tag).filter(
            func.lower(Tag.name).contains(query_text)
        ).all()
        
        articles_with_matching_tags = []
        for tag in matching_tags:
            articles_with_matching_tags.extend(tag.articles)
            
        # 合并结果并去重
        all_matching_articles = list(set(articles_with_matching_title_or_content + articles_with_matching_tags))
        return all_matching_articles

    def create_article(self, article:Article):
        query = Select(Article).where(Article.title == article.title)
        is_exist = db.session.execute(query).scalar()
        if is_exist:
            return article, '同标题文章已经存在'

        db.session.add(article)
        db.session.commit()

        return article,None

    def update_article(self, updated_article:Article):
        is_exist = db.session.get(Article,updated_article.id)
        if not is_exist:
            return updated_article, '文章不存在'
        query = Select(Article).where(and_(Article.title == updated_article.title,Article.id != updated_article.id))
        is_exist_same_title = db.session.execute(query).all()
        if is_exist_same_title:
            return updated_article, '同标题文章已存在'

        is_exist.title = updated_article.title
        is_exist.content = updated_article.content
        is_exist.tags = updated_article.tags
        is_exist.update_time = func.now()
        db.session.commit()

        return updated_article,None

    def delete_article(self, article_id:int):
        query = Select(Article).where(Article.id == article_id)
        is_exist = db.session.execute(query).scalar()
        if not is_exist:
            return False,'找不到要删除的文章'
        db.session.delete(is_exist)
        db.session.commit()
        return True,None