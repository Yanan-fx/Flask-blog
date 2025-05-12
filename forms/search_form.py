from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    query = StringField('搜索', validators=[DataRequired()])
    submit = SubmitField('搜索')
    
    # 在构造函数中禁用CSRF保护，这样可以直接在导航栏使用GET请求
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs) 