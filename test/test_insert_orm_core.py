from routes import db
from models.article import Article
from sqlalchemy import insert, create_engine, Table, MetaData
from routes import app
from sqlalchemy.orm import Session
from models.user import User
import traceback

engine = create_engine('mysql+mysqldb://root:root@localhost:3306/flask_blog')

def insert_orm():
    article = [
        Article(
            title="mapped使用方法",
            content="""name: Mapped[str] = mapped_column(String(128), unique = Ture , nullable = False)"""
        ),
        Article(
            title="back_populates 双向关联 ",
            content="""name: department: Mapped[Department] = relationship(lazy = False, back_populates = "employees" )""",
        ),
        Article(
            title = "11",
            content = "asdf"
        )
    ]
    db.session.add_all(article)
    db.session.commit()

def insert_core():
    with Session(engine) as session:
        # 获取Article对应的Table对象
        articles_table = Article.__table__
        
        # 使用Table对象构建insert语句
        stmt = insert(articles_table).values([
            {
                "title": "flask如何连接数据库",
                "content": "app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:root@localhost:3306/flask_blog'".encode('utf8'),
            },
            {
                "title": "sqlalchemy关联表",
                "content": """column设置中的 sqlalchemy.ForeignKey("department_table.id")""".encode("utf8")
            }
        ])
        session.execute(stmt)
        session.commit()

def check_articles():
    articles = Article.query.all()
    if not articles:
        print("没有文章")
        return

    print(f"数据库中有 {len(articles)} 篇文章：")
    for article in articles:
        print(f"ID: {article.id}, title: {article.title}, content: {article.content}")

def create_user_table():
    with app.app_context():
        print("开始创建用户表...")
        # 创建表
        db.create_all()
        print("表结构已创建")

def insert_user_table():
    user = [
        User(
            password = "root",
            fullname = "Yanan",
            description = "我是管理员雅楠",
            role = "admin"
        ),
        User(
            username="114514",
            password="114514",
            fullname="pp",
            description="我是颠佬",
            role="user"
        )
    ]
    db.session.add_all(user)
    db.session.commit()

if __name__ == '__main__':

    with app.app_context():
        # try:
        #     insert_orm()
        #     print("orm方式插入成功")
        # except Exception as e:
        #     print(f"orm插入失败: {e}")
        #     import traceback
        #     traceback.print_exc()
        #
        # try:
        #     insert_core()
        #     print("Core插入成功")
        # except Exception as e:
        #     print(f"Core插入失败: {e}")
        #     import traceback
        #     traceback.print_exc()
        try:
            create_user_table()
        except Exception as e:
            print(f"创建user表失败: {e}")
            traceback.print_exc()

        try:
            insert_user_table()
        except Exception as e:
            print(f"user表插入数据失败: {e}")
            traceback.print_exc()
        # check_articles()
