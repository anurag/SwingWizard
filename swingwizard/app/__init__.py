from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'base.login'
login.login_message = ('Please log in to access this page.')


def create_app(config_class=Config):
    app = Flask(__name__,
                static_url_path='',
                static_folder='static',
                template_folder='templates')
    app.config.from_object(config_class)
    app.config['UPLOAD_FOLDER']
    app.config['ALLOWED_EXTENSIONS']

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)

    from app.base import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

from app.base import routes
from app import models
