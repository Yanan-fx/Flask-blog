from os import abort

from flask_login import login_required, logout_user

from forms.login_form import LoginForm
from models.article import Article
from routes import app
from flask import render_template, flash, redirect, url_for
from services.article_service import ArticleService
from services.user_service import UserService


@app.route('/')
@app.route('/index.html')
def home_page():
    articles = ArticleService().get_articles()
    return render_template('index.html', articles=articles)

@app.route('/about.html')
def about_page():
    return render_template('about.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        result, user = UserService().do_login(form.username.data, form.password.data)
        if result:
            flash(f'欢迎{user.fullname}回来',category='success')
            return redirect(url_for('home_page'))
        else:
            flash('用户名或密码错误,请重试！',category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('您已成功退出登录', category='info')
    return redirect(url_for('home_page'))

@app.route('/article/<article_id>.html')
def article_page(article_id):
    article = ArticleService().get_article(article_id)
    if article:
        return render_template('article.html', article=article)
    else:
        abort(404)
