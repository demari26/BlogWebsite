from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from flask import Blueprint, flash, render_template, redirect, url_for
from forms import CreatePostForm, RegistrationForm, LoginForm, CommentForm
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash


guest = Blueprint('guest_views', __name__, template_folder='templates', static_folder='static')


@guest.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user:
            flash('Email already exists!')
            return redirect(url_for('login'))
        new_user = User(
            email = form.email.data,
            name = form.name.data,
            password = generate_password_hash(form.password.data, 'scrypt', 8)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect('/')
    return render_template("guest/register.html", form=form)


@guest.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if not user:
            flash("You're email does not exists")
            return redirect(url_for('login'))
        if not check_password_hash(user.password, form.password.data):
            flash('Invalid password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('get_all_posts'))
    return render_template("guest/login.html", form=form)


@guest.route("/about")
def about():
    return render_template("about.html")


@guest.route("/contact")
def contact():
    return render_template("contact.html")