from flask_login import current_user, logout_user, login_required
from flask import Blueprint, flash, render_template, redirect, url_for, make_response, request
from forms import CreatePostForm, CommentForm, GenerateBlogForm
from models import db, BlogPost, Comment
from middleware import admin_only
import datetime as date
import requests

authenticated_user = Blueprint('user_views', __name__, template_folder='templates', static_folder='static')

@authenticated_user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_views.get_all_posts'))


@authenticated_user.route('/')
@login_required
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@authenticated_user.route("/post/<int:post_id>", methods=['POST','GET'])
@login_required
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You must log in first!")
            return redirect(url_for('login'))
        new_comment = Comment(
            text = comment_form.comment.data,
            comment_author = current_user,
            parent_post = requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
        
        return redirect(url_for('user_views.show_post', post_id=post_id))
    return render_template("post.html", post=requested_post, comment_form=comment_form)


@authenticated_user.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_only
def add_new_post():
    if request.cookies.get('body'):
        form = CreatePostForm(
            body = request.cookies.get('body'),
            title = request.cookies.get('title')
        )
    else:
        form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.datetime.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        response = make_response(redirect(url_for("user_views.get_all_posts")))
        response.delete_cookie('body')
        response.delete_cookie('title')
        return response
    return render_template("make-post.html", form=form)


@authenticated_user.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@authenticated_user.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@authenticated_user.route('/generate-blog', methods=['GET','POST'])
@login_required
def generate_blog():
    form = GenerateBlogForm()
    if form.validate_on_submit():
        response = requests.get(f"http://127.0.0.1:5000{url_for('ai_routes.generate_blog', title=form.title.data)}")
        data = response.json()
        form = CreatePostForm(
            title = data["title"],
            body = data["message"]
        )
        response = redirect(url_for('user_views.add_new_post'))
        response.set_cookie('body', data["message"])
        response.set_cookie('title', data["title"])
        return response
    return render_template('generate-blog.html', form=form)