from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models.user import User
from routes import db
from sqlalchemy import Select

class RegisterForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired()])
    password_confirm = PasswordField(label='确认密码', validators=[DataRequired(), EqualTo('password', message='两次输入的密码不一致')])
    fullname = StringField(label='昵称', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField(label='个人描述')
    submit = SubmitField(label='注册')

    def validate_username(self, username):
        query = Select(User).where(User.username == username.data)
        user = db.session.execute(query).scalar()
        if user:
            raise ValidationError('该用户名已被注册，请更换一个') 