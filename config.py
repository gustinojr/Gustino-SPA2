import os

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///gustino.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    OWNER_CHAT_ID = os.environ.get("OWNER_CHAT_ID")
    TELEGRAM_BOT_USERNAME = os.environ.get("TELEGRAM_BOT_USERNAME")

    ADMIN_KEY = os.environ["ADMIN_KEY"]
    LOG_PATH = os.environ.get("LOG_PATH", "app.log")

    DEFAULT_PROMO_CODES = ["GUSTINO2025", "20121997", "VIP2025"]
