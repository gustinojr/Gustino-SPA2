import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
import logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from .database_init import initialize_database
        initialize_database()

    setup_logging(app)
    register_blueprints(app)

    return app

def setup_logging(app):
    log_path = app.config.get("LOG_PATH", "app.log")
    handler = RotatingFileHandler(log_path, maxBytes=5_000_000, backupCount=3)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

def register_blueprints(app):
    from .routes.home import home_bp
    from .routes.register import register_bp
    from .routes.booking import booking_bp
    from .routes.webhook import webhook_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(webhook_bp)
