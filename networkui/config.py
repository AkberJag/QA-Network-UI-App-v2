"""Application Configuration."""

import os


class Config:
    """
    Base configuration. Contains default configuration settings + configuration settings
    applicable to all environments.
    """

    SECRET_KEY = os.environ.get("CONDUIT_SECRET", "secret-key")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration."""

    DB_NAME = "dev.db"
    DB_PATH = os.path.join(Config.BASE_DIR, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"


class ProductionConfig(Config):
    """Production Config"""


# this flag is to prevent multiple users from running script simultaniously
# TODO: Ask help for a better implementaion of this.
is_a_script_running = False
