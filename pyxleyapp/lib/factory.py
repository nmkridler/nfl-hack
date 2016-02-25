import os
import logging
from flask import Flask
import datetime
from decimal import Decimal

def get_static_folder():
    instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    return instance_path, os.path.join(instance_path, 'static')

def create_app():
    instance_path, static_folder = get_static_folder()
    app = Flask(__name__, instance_path=instance_path,
                          instance_relative_config=True,
                          static_folder=static_folder,
                          template_folder=os.path.join(instance_path, 'templates'))

    # Overwrite all default Flask handlers
    handler = logging.StreamHandler()
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    app.logger.handlers = [handler]

    return app


