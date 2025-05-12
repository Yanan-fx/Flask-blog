from flask_login import current_user, login_required
from flask import redirect, url_for, flash, request

from forms.comment_form import CommentForm
from models.comment import Comment
from routes import app
from services.comment_service import CommentService

@app.route('/comment/add/<article_id>', methods=['POST'])
@login_required
def add_comment_with_id(article_id):
    """添加评论（使用URL参数获取文章ID）"""
    # 从请求中获取评论内容
    content = request.form.get('content')
    
    # 验证数据是否存在
    if not content or not content.strip():
        flash('评论内容不能为空', 'danger')
        return redirect(url_for('article_page', article_id=article_id))
    
    try:
        # 创建评论
        comment = Comment()
        comment.content = content
        comment.article_id = int(article_id)
        comment.user_id = current_user.id
        
        CommentService().create_comment(comment)
        flash('评论发表成功！', 'success')
    except Exception as e:
        flash(f'评论发表失败: {str(e)}', 'danger')
    
    # 重定向回文章页面
    return redirect(url_for('article_page', article_id=article_id))

@app.route('/comment/delete/<comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """删除评论"""
    comment_service = CommentService()
    comment = comment_service.get_comment(int(comment_id))
    
    if not comment:
        flash('评论不存在', 'danger')
        return redirect(request.referrer or url_for('home_page'))
    
    # 检查权限
    if not comment_service.can_delete_comment(int(comment_id), current_user.id, getattr(current_user, 'is_admin', False)):
        flash('没有权限删除此评论', 'danger')
        return redirect(request.referrer or url_for('home_page'))
    
    # 删除评论
    if comment_service.delete_comment(int(comment_id)):
        flash('评论已删除', 'success')
    else:
        flash('删除评论失败', 'danger')
    
    # 返回到之前的页面
    return redirect(request.referrer or url_for('home_page')) 