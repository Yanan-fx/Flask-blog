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
        
    def register_user(self, username:str, password:str, fullname:str, description:str=None) -> tuple[bool, str]:
        # 检查用户名是否已存在
        query = Select(User).where(User.username == username)
        existing_user = db.session.execute(query).scalar()
        if existing_user:
            return False, "用户名已被注册"
        
        # 创建新用户
        new_user = User()
        new_user.username = username
        new_user.password = password
        new_user.fullname = fullname
        new_user.description = description
        new_user.role = "user"  # 默认角色
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return True, "注册成功"
        except Exception as e:
            db.session.rollback()
            return False, f"注册失败: {str(e)}"