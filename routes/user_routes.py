from os import abort

from flask_login import login_required, logout_user, current_user

from forms.comment_form import CommentForm
from forms.delete_article_form import DeleteArticleForm
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.search_form import SearchForm
from models.article import Article
from routes import app
from flask import render_template, flash, redirect, url_for, request

from routes.admin_routes import admin_required
from services.article_service import ArticleService
from services.comment_service import CommentService
from services.user_service import UserService


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html' , methods=['GET', 'POST'])
def home_page():
    articles = ArticleService().get_articles()

    if current_user.is_authenticated and current_user.is_admin:
        delete_article_form = DeleteArticleForm()
        if delete_article_form.validate_on_submit():
            result,error_meg = ArticleService().delete_article(int(delete_article_form.article_id.data))
            if result:
                flash(f'删除文章成功', category='success')
                return redirect(url_for('home_page'))
            else:
                flash(f'删除文章失败：{error_meg}', category='danger')

        return render_template('index.html', articles=articles,delete_article_form=delete_article_form)
    else:
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

@app.route('/register.html', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # 注册用户
        result, message = UserService().register_user(
            username=form.username.data,
            password=form.password.data,
            fullname=form.fullname.data,
            description=form.description.data
        )
        
        if result:
            flash(message, 'success')
            return redirect(url_for('login_page'))
        else:
            flash(message, 'danger')
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('您已成功退出登录', category='info')
    return redirect(url_for('home_page'))

@app.route('/article/<article_id>.html')
def article_page(article_id):
    try:
        # 确保article_id是整数
        article_id_int = int(article_id)
        article = ArticleService().get_article(article_id_int)
        if article:
            # 获取评论
            comments = CommentService().get_comments_by_article(article_id_int)
            
            # 创建评论表单
            comment_form = CommentForm()
            
            return render_template('article.html', 
                                article=article, 
                                comments=comments,
                                comment_form=comment_form)
        else:
            flash('文章不存在', 'danger')
            return redirect(url_for('home_page'))
    except ValueError:
        flash('无效的文章ID', 'danger')
        return redirect(url_for('home_page'))

@app.route('/search')
def search():
    """搜索文章"""
    query = request.args.get('query', '')
    if not query.strip():
        flash('请输入搜索内容', 'warning')
        return redirect(url_for('home_page'))
        
    articles = ArticleService().search_articles(query)
    
    # 如果用户是管理员，添加删除表单
    if current_user.is_authenticated and current_user.is_admin:
        delete_article_form = DeleteArticleForm()
        return render_template('search_results.html', articles=articles, query=query, delete_article_form=delete_article_form)
    else:
        return render_template('search_results.html', articles=articles, query=query)
