from models.article import Article
from routes import db
from sqlalchemy import Select

class ArticleService:

    def get_article(self, id):
        return db.session.get(Article,id)

    def get_articles(self):
        query = Select(Article)
        return db.session.scalars(query).all()

    def create_article(self, article:Article):
        db.session.add(article)
        db.session.commit()
        return article