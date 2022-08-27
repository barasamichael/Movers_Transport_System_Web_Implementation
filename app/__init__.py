#import flask extensions

import flask
import flask_bootstrap
import flask_moment
import flask_sqlalchemy
from flask_login import LoginManager
import flask_mail

from config import config

bootstrap = flask_bootstrap.Bootstrap()
mail = flask_mail.Mail()
db = flask_sqlalchemy.SQLAlchemy()
moment = flask_moment.Moment()

login_manager = LoginManager()
login_manager.login_view = 'authentication.login_user'


def create_app(config_name):
    """
    Application initialization.
    Takes as an argument one of the configuration classes defined in config.py
    """

    app = flask.Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .register import register
    app.register_blueprint(register, url_prefix = '/register')

    from .records import records as records_blueprint
    app.register_blueprint(records_blueprint, url_prefix = '/records')

    from .authentication import authentication as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/auth')

    from .profiles import profiles as profiles_blueprint
    app.register_blueprint(profiles_blueprint, url_prefix = '/profile') 

    return app
