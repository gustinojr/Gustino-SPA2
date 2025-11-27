from flask import Blueprint, request, jsonify, current_app
from app.models import User, PromoCode
from app import db
from app.telegram import tg_send

telegram_bp = Blueprint("telegram", __name__, url_prefix="/telegramWebhook")

@telegram_bp.post("/")
def telegram_webhook():
    data = request.json
    if "message" not in data:
        return jsonify({"status": "ignored"})

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    if text.startswith("/start"):
        promo_code = text.replace("/start", "").strip()
        if not promo_code:
            tg_send(chat_id, "Per favore invia un codice valido.")
            return "ok"

        promo_row = PromoCode.query.filter_by(code=promo_code).first()
        if not promo_row:
            tg_send(chat_id, "❌ Codice inesistente.")
            return "ok"

        # Collega chat_id all'utente
        user = User.query.filter_by(promo_code=promo_code).first()
        if user:
            user.chat_id = chat_id
        else:
            user = User(name="Utente", promo_code=promo_code, chat_id=chat_id)
            db.session.add(user)
        db.session.commit()

        promo_row.redeemed = True
        promo_row.assigned_user_id = user.id
        db.session.commit()

        tg_send(chat_id, "🎉 Benvenuto! Torna sul sito per completare la registrazione.")
        return "ok"

    return "ignored"
