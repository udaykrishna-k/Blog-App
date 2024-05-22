from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    content = TextAreaField("Content", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("submit")