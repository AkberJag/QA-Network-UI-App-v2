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

    # create the db folder to avoid the error > sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file
    if not os.path.exists(os.path.join(BASE_DIR, "db")):
        os.makedirs(os.path.join(BASE_DIR, "db"))

    DB_FOLDER = os.path.join(BASE_DIR, "db")


class DevelopmentConfig(Config):
    """Development configuration."""

    DB_NAME = "dev.sqlite"
    DB_PATH = os.path.join(Config.DB_FOLDER, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"


class ProductionConfig(Config):
    """Production Config"""


# this flag is to prevent multiple users from running script simultaniously
# ? Ask help for a better implementaion of this.
global is_a_script_running
is_a_script_running = False
