from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysupersecretpassword"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1ds15ec046@localhost/blogapp"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "warning"

from flaskblog import routes