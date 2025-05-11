from flask_login import login_user
from sqlalchemy import Select
from typing import Tuple, Any
from models.user import User
from routes import db


class UserService:
    def do_login(self, username:str, password:str) -> tuple[bool, Any] | tuple[bool, None]:
        query = Select(User).where(User.username == username)
        attempted_user = db.session.scalar(query)

        if attempted_user and attempted_user.check_password_correction(attempted_password = password):
            login_user(attempted_user) #关键函数,自动完成用户登录后设置session放用户
            return True, attempted_user
        return False, None