from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config.from_pyfile("config.py")
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
Migrate(app, db)

from musteri import musteri_bp
from guncel_modul import guncel_modul
app.register_blueprint(musteri_bp)
app.register_blueprint(guncel_modul)
from . import route
