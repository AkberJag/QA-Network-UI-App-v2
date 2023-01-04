"""The app module, containing the app factory function."""
from config import DevelopmentConfig
from flask import Flask


def create_app(config_object=DevelopmentConfig):
    """Create application factory, as explained here: https://flask.palletsprojects.com/en/2.2.x/patterns/appfactories/

    Args:
        config_object: The configuration object to use. Defaults to DevelopmentConfig.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    return app
