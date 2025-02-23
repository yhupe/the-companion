import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask


from application.config import config
from application.views.main_views import main
from application.views.whatsapp import whatsapp

from application.db.db_init import db, migrate

base_dir = Path(__name__).parent.parent
load_dotenv()


def create_app():
    app = Flask(__name__)

    CONFIG_NAME = os.environ.get("FLASK_ENV", "development")
    DATABASE_URL = os.getenv("DATABASE_URL")
    app.config.from_object(
        config[CONFIG_NAME]()
    )

    if not CONFIG_NAME:
        print("DATABASE_URL is not set! Using fallback default.")
        DATABASE_URL = "sqlite:///default.db"
    else:
        print(f"Using database: {DATABASE_URL}")

    # Use it in your Flask config
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

    app.logger.info(f"App started - Config name: {CONFIG_NAME}")

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(
        app.config.get("LOG_LEVEL", logging.DEBUG)
    )

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    db.init_app(app)
    migrate.init_app(app, db,)

    app.logger.addHandler(handler)

    app.logger.info(f"App started - Config name: {CONFIG_NAME}")

    app.register_blueprint(main)
    app.register_blueprint(whatsapp)

    return app
