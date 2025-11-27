from flask import Blueprint, request, jsonify
from ..models import PromoCode, User
from ..telegram import tg_send
from .. import db

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.post("/telegramWebhook")
def telegram_webhook():
    data = request.json
    if "message" not in data:
        return jsonify({"status": "ignored"})

    msg = data["message"]
    text = msg.get("text", "")
    chat_id = msg["chat"]["id"]

    if not text.startswith("/start"):
        return jsonify({"status": "ignored"})

    promo = text.replace("/start", "").strip()
    if not promo:
        tg_send(chat_id, "Per favore invia un codice valido.")
        return "ok"

    promo_row = PromoCode.query.filter_by(code=promo).first()
    if not promo_row:
        tg_send(chat_id, "❌ Codice inesistente.")
        return "ok"

    user = User.query.filter_by(promo_code=promo).first()

    if user and user.chat_id and user.chat_id != chat_id:
        tg_send(chat_id, "⚠ Questo codice è già stato utilizzato.")
        return "ok"

    if not user:
        user = User(name="Utente", promo_code=promo, chat_id=chat_id)
        db.session.add(user)
    else:
        user.chat_id = chat_id

    promo_row.redeemed = True
    promo_row.assigned_user_id = user.id

    db.session.commit()

    tg_send(chat_id, "🎉 Benvenuto! Code collegato. Torna sul sito per completare la prenotazione.")
    return "ok"
