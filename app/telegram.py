import requests
from flask import current_app

def tg_send(chat_id, text):
    if not chat_id:
        current_app.logger.warning("Cannot send Telegram message: chat_id is None")
        return

    token = current_app.config["TELEGRAM_BOT_TOKEN"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        response = requests.post(url, data={"chat_id": chat_id, "text": text}, timeout=5)
        if not response.ok:
            current_app.logger.error(f"Telegram error: {response.text}")
    except Exception as e:
        current_app.logger.error(f"Telegram send ERROR: {e}")
