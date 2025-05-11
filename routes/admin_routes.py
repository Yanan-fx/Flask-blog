import flask
from flask_login import login_required

from forms.article_form import ArticleForm
from models.article import Article
from routes import app, db
from flask import render_template, redirect, url_for

from services.article_service import ArticleService


@app.route('/editartical.html', methods=['GET', 'POST'])
@login_required #用来验证登录后的用户才可使用下方的方法
def create_article_page():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article()
        article.title = form.title.data
        article.content = form.content.data

        try:
            ArticleService().create_article(article)
            flask.flash(f'成功发布文章{article.title}', 'success')
            return redirect(url_for('home_page'))
        except Exception as e:
            from sqlalchemy.exc import IntegrityError
            db.session.rollback()  # 回滚事务
            if isinstance(e, IntegrityError) and "Duplicate entry" in str(e) and "for key 'title'" in str(e):
                flask.flash(f'发布失败: 文章标题已存在，请使用其他标题', 'danger')
            else:
                flask.flash(f'发布失败: {e}', 'danger')

    return render_template('editartical.html', form=form)