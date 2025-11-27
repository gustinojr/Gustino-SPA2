import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.telegram import tg_send  # funzione Telegram centralizzata

db = SQLAlchemy()

def create_app():
    # ==========================
    # CREATE FLASK APP
    # ==========================
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # ==========================
    # LOGGING
    # ==========================
    LOG_PATH = os.environ.get("LOG_PATH", "app.log")
    handler = RotatingFileHandler(LOG_PATH, maxBytes=5_000_000, backupCount=3, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)
    app.logger.addHandler(console)

    # ==========================
    # DATABASE
    # ==========================
    db.init_app(app)

    with app.app_context():
        from app.models import User, Reservation, PromoCode

        # crea tabelle se non esistono
        db.create_all()

        # inizializza promo codes
        default_codes = getattr(app.config, "DEFAULT_PROMO_CODES", [])
        for code in default_codes:
            if not PromoCode.query.filter_by(code=code).first():
                db.session.add(PromoCode(code=code))
        db.session.commit()

    # ==========================
    # REGISTER BLUEPRINTS
    # ==========================
    from app.routes.home import home_bp
    from app.routes.register import register_bp
    from app.routes.booking import booking_bp
    from app.routes.telegram_webhook import telegram_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(telegram_bp)

    # ==========================
    # TELEGRAM BOT INIT
    # ==========================
    app.logger.info("App initialized successfully with Telegram bot support.")

    return app
