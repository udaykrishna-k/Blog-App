from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required

from forms.blog_post_form import BlogPostForm
from forms.login_form import LoginForm
from forms.signup_form import SignUp
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysupersecretpassword"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1ds15ec046@localhost/blogapp"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"({self.first_name + ' ' + self.last_name}, , {self.username}, {self.email})"

class BlogPostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

with app.app_context():
    db.create_all()

@app.route("/")
def home_page():
    return render_template("base.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash("Login successfull")
            login_user(user)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home_page'))
        flash("Check username and Password")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))

@app.route("/sign_up",methods=["GET","POST"])
def sign_up():
    form = SignUp()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email Id is already registered")
        else:
            password_hash = generate_password_hash(form.password.data)
            user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=password_hash)
            db.session.add(user)
            db.session.commit()
            form.first_name.data = ''
            form.last_name.data = ''
            form.username.data = ''
            form.email.data = ''
            form.password.data = ''
            form.confirm_password.data = ''
            flash("User added succesfully")
            return redirect(url_for("login"))
    return render_template("sign_up.html", form=form)

@app.route("/account")
@login_required
def account():
    return render_template("account.html")

@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post_model = BlogPostModel(title=form.title.data, author=form.author.data, content=form.content.data)
        db.session.add(blog_post_model)
        db.session.commit()
        form.title.data = ''
        form.author.data = ''
        form.content.data = ''
        flash("Added post successfully")
    return render_template("add_post.html", form=form)

@app.route("/blog_posts")
def blog_posts():
    list_of_blog_posts = BlogPostModel.query.all()
    return render_template('blog_posts.html', list_of_blog_posts=list_of_blog_posts)

@app.route("/posts/<int:id>")
def view_post(id):
    post = BlogPostModel.query.get(id)
    return render_template("view_post.html", post=post, id=id)

@app.route("/edit_post/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    post = BlogPostModel.query.get(id)
    form = BlogPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        form.title.data = ''
        form.author.data = ''
        form.content.data = ''
        flash("Post edited successfully")
        return redirect(url_for("view_post", id=id))
    form.title.data = post.title
    form.author.data = post.author
    form.content.data = post.content
    return render_template("edit_post.html", form=form)