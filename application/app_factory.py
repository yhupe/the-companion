import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask


from application.config import config
from application.views.main_views import main

base_dir = Path(__name__).parent.parent
load_dotenv()


def create_app():
    app = Flask(__name__)

    config_name = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(
        config[config_name]()
    )



    app.logger.info(f"App started - Config name: {config_name}")

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(
        app.config.get("LOG_LEVEL", logging.DEBUG)
    )

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    app.logger.info(f"App started - Config name: {config_name}")

    app.register_blueprint(main)

    return app
