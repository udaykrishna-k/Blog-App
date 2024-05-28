from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from flaskblog import db, app, login_manager
from flaskblog.forms import LoginForm, SignUpForm, PostForm, UpdateAccountForm
from flaskblog.models import User, Post


@app.route("/")
def home_page():
    return render_template("home_page.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash("Login successfull", 'success')
            login_user(user)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home_page'))
        flash("Check username and Password", "success")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))

@app.route("/sign_up",methods=["GET","POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email Id is already registered", "error")
        else:
            password_hash = generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data, password=password_hash)
            db.session.add(user)
            db.session.commit()
            form.username.data = ''
            form.email.data = ''
            form.password.data = ''
            form.confirm_password.data = ''
            flash("User added succesfully", "success")
            return redirect(url_for("login"))
    return render_template("sign_up.html", form=form)

@app.route("/account")
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Updated succesfully", "success")
        return redirect(url_for("account"))
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", form=form)

@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        blog_post_model = Post(title=form.title.data, author=form.author.data, content=form.content.data)
        db.session.add(blog_post_model)
        db.session.commit()
        form.title.data = ''
        form.author.data = ''
        form.content.data = ''
        flash("Added post successfully", "success")
    return render_template("add_post.html", form=form)

@app.route("/blog_posts")
def blog_posts():
    list_of_blog_posts = Post.query.all()
    return render_template('blog_posts.html', list_of_blog_posts=list_of_blog_posts)

@app.route("/posts/<int:id>")
def view_post(id):
    post = Post.query.get(id)
    return render_template("view_post.html", post=post, id=id)

@app.route("/edit_post/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    post = Post.query.get(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        form.title.data = ''
        form.author.data = ''
        form.content.data = ''
        flash("Post edited successfully", "success")
        return redirect(url_for("view_post", id=id))
    form.title.data = post.title
    form.author.data = post.author
    form.content.data = post.content
    return render_template("edit_post.html", form=form)