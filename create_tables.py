from routes import db, app
from models.tag import Tag
from models.article import Article
from models.user import User
from models.comment import Comment

# 创建数据库上下文
with app.app_context():
    # 创建所有表
    db.create_all()
    print("数据库表已创建/更新") 