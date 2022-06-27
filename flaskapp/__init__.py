
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'


app = Flask(__name__)  # wsgi application instance

app.config['SECRET_KEY'] = '4ff07c684c1963c2e1fa8a63a0fbee021a49285e37a8efd475950113caf868f7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.anonymous_user = Anonymous
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ayushverma01911@gmail.com'
app.config['MAIL_PASSWORD'] = 'somethingweird'
mail = Mail(app)
from flaskapp import routes
