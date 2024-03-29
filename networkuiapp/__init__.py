"""Main application package containing the app factory function."""

from flask import Flask

from networkuiapp import public
from networkuiapp import ipaddress
from networkuiapp import networktemplate

from networkuiapp.extensions import db
from networkuiapp.extensions import migrate

from networkuiapp.config import DevelopmentConfig


def create_app(config_object=DevelopmentConfig):
    """Create application factory, as explained here: https://flask.palletsprojects.com/en/2.2.x/patterns/appfactories/

    Args:
        config_object: The configuration object to use. Defaults to DevelopmentConfig.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(ipaddress.views.blueprint)
    app.register_blueprint(networktemplate.views.blueprint)
