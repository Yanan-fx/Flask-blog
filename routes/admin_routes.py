from functools import wraps
from turtledemo.sorting_animate import enable_keys

import flask
from flask_login import login_required, current_user

from forms.article_form import ArticleForm
from models.article import Article
from models.tag import Tag
from routes import app, db
from flask import render_template, redirect, url_for, flash, request

from services.article_service import ArticleService
from services.tag_service import TagService

# 创建管理员权限检查装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin or not current_user.is_authenticated:
            flash('需要管理员权限','danger')
            return redirect(url_for('home_page'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/editarticle.html', methods=['GET', 'POST'])
@login_required #用来验证登录后的用户才可使用下方的方法
def create_article_page():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article()
        article.title = form.title.data
        article.content = form.content.data
        
        # 处理标签
        if form.tags.data:
            article.tags = TagService().get_or_create_tags(form.tags.data)

        try:
            the_article,error_meg =ArticleService().create_article(article)
            if error_meg:
                flash(f'发布失败: {error_meg}', 'danger')
            else:
                flash(f'成功发布文章{article.title}', 'success')
                return redirect(url_for('home_page'))
        except Exception as e:
                flash(f'发布失败: {e}', 'danger')

    return render_template('editarticle.html', form=form,is_edit=False)

@app.route('/editarticle/<article_id>.html', methods=['GET', 'POST'])
@login_required #用来验证登录后的用户才可使用下方的方法
@admin_required  # 只有管理员才能编辑文章
def edit_article_page(article_id:str):
    form = ArticleForm()

    if request.method == 'GET':
        try:
            article = ArticleService().get_article(int(article_id))
            if not article:
                flash(f'要修改的文章not found:', 'danger')
                return redirect(url_for('home_page'))
            else:
                form.title.data = article.title
                form.content.data = article.content
                form.tags.data = article.get_tags_string()
        except Exception as e:
            flash(f'获取文章失败: {e}', 'danger')
            return redirect(url_for('home_page'))

    if form.validate_on_submit():
        try:
            updated_article = Article()
            updated_article.id = int(article_id)
            updated_article.title = form.title.data
            updated_article.content = form.content.data
            
            # 处理标签
            if form.tags.data:
                updated_article.tags = TagService().get_or_create_tags(form.tags.data)

            the_article,error_meg = ArticleService().update_article(updated_article)
            if error_meg:
                flash(f'修改文章失败: {error_meg}', 'danger')
            else:
                flash(f'成功修改文章{updated_article.title}', 'success')
                return redirect(url_for('home_page'))
        except Exception as e:
            flash(f'修改失败: {e}', 'danger')

    return render_template('editarticle.html', form=form,is_edit=True)
    
@app.route('/tag/<tag_id>')
def articles_by_tag(tag_id):
    """显示指定标签的所有文章"""
    articles = ArticleService().get_articles_by_tag(tag_id)
    tag = db.session.get(Tag, tag_id)
    
    # 为管理员用户提供删除表单
    if current_user.is_authenticated and current_user.is_admin:
        from forms.delete_article_form import DeleteArticleForm
        delete_article_form = DeleteArticleForm()
        return render_template('index.html', articles=articles, filter_tag=tag, delete_article_form=delete_article_form)
    else:
        return render_template('index.html', articles=articles, filter_tag=tag)