from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../assets',
            static_url_path='/assets')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:root@localhost:3306/flask_blog'
app.config['SECRET_KEY'] = '1141541919810'

db = SQLAlchemy(app) #操作数据库，映射数据库
login_manager = LoginManager(app)

from routes import user_routes
from routes import admin_routes
from routes import comment_routes

