from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from forms.signup_form import SignUp
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysupersecretpassword"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1ds15ec046@localhost/blogapp"

db = SQLAlchemy(app)
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

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
