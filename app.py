from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from forms.blog_post_form import BlogPostForm
from forms.signup_form import SignUp
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysupersecretpassword"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1ds15ec046@localhost/blogapp"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

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

@app.route("/sign_up",methods=["GET","POST"])
def sign_up():
    form = SignUp()
    if form.validate_on_submit():
        if UserModel.query.filter_by(email=form.email.data).first():
            flash("Email Id is already registered")
        else:
            password_hash = generate_password_hash(form.password.data)
            user = UserModel(name=form.name.data, email=form.email.data, password=password_hash)
            db.session.add(user)
            db.session.commit()
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
            flash("User added succesfully")
    return render_template("sign_up.html", form=form)

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