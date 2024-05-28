from datetime import datetime

from flask_login import UserMixin

from flaskblog import db, app


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    image_file = db.Column(db.String(200), default='default.jpg', nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"BlogPostModel({self.title}, '{self.author}', '{self.date_added}')"

with app.app_context():
    db.create_all()
