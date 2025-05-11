from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired


class DeleteArticleForm(FlaskForm):
    article_id = HiddenField('article_id', validators=[DataRequired()])
    submit = SubmitField(label='删除')