from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length

class CommentForm(FlaskForm):
    content = TextAreaField('评论内容', validators=[DataRequired(), Length(min=1, max=1000)])
    article_id = HiddenField('文章ID', validators=[DataRequired()])
    submit = SubmitField('发表评论') 