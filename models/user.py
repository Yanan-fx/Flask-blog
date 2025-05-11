from flask_login import UserMixin
from routes import db,login_manager
from sqlalchemy import Integer, String, BLOB, TIMESTAMP,func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


@login_manager.user_loader # Flask-Login 的必需配置
def load_user(user_id):
    return db.session.get(User,user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=True)

    def check_password_correction(self, attempted_password):
        return self.password == attempted_password
