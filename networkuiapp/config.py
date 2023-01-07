"""Application Configuration."""

import os


class Config:
    """
    Base configuration. Contains default configuration settings + configuration settings
    applicable to all environments.
    """

    # SECRET_KEY = os.environ.get("CONDUIT_SECRET", "secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "adsadsads"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig(Config):
    """Development configuration."""

    DB_NAME = "dev.sqlite"
    DB_PATH = os.path.join(Config.BASE_DIR, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"


class ProductionConfig(Config):
    """Production Config"""


# this flag is to prevent multiple users from running script simultaniously
# ? Ask help for a better implementaion of this.
global is_a_script_running
is_a_script_running = False
