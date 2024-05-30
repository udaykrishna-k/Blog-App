from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.simple import EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from wtforms.widgets import TextArea
import email_validator

from flaskblog.models import User


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    content = TextAreaField("Content", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("submit")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("submit")

class SignUpForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField("email", validators=[DataRequired(), Email()])
    password = PasswordField("Enter Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("submit")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash("This username is already taken")
            raise ValidationError("This username is already taken")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("This email is already taken")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    image_file = FileField("Update profile pic", validators=[FileAllowed(["jpeg", "png", "jpg"])])
    submit = SubmitField("update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                flash("This username is already taken")
                raise ValidationError("This username is already taken")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("This email is already taken")