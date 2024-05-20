from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from forms.signup_form import SignUp

app = Flask(__name__)
# db = SQLAlchemy(app)

app.config["SECRET_KEY"] = "mysupersecretpassword"

@app.route("/")
def home_page():
    return "Hello World!!!"

@app.route("/add_user",methods=["GET","POST"])
def add_user():
    form = SignUp()
    if form.validate_on_submit():
        form.name.data = ''
        form.email.data = ''
        form.password.data = ''
        flash("User added succesfully")
    return render_template("sign_up.html", form=form)
