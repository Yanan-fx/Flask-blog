from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Optional


class ArticleForm(FlaskForm):
    title = StringField(label="标题", validators=[DataRequired()])
    content = TextAreaField(label="内容", validators=[DataRequired()])
    tags = StringField(label="标签", validators=[Optional()], 
                      description="多个标签请用逗号分隔，例如：技术,学习,Python")
    submit = SubmitField(label="保存")