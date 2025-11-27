@app.post("/telegramWebhook")
def telegram_webhook():
    data = request.json

    if "message" not in data:
        return jsonify({"status": "ignored"})

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    if text.startswith("/start"):
        promo = text.replace("/start", "").strip()
        promo_row = PromoCode.query.filter_by(code=promo).first()

        if not promo_row:
            tg_send(chat_id, "❌ Codice inesistente.")
            return "ok"

        # assegna chat_id all’utente
        user = User.query.filter_by(promo_code=promo).first()
        if not user:
            user = User(name="Utente", promo_code=promo, chat_id=chat_id)
            db.session.add(user)
            db.session.commit()  # serve per avere user.id
        else:
            user.chat_id = chat_id
            db.session.commit()

        promo_row.redeemed = True
        promo_row.assigned_user_id = user.id
        db.session.commit()

        # Messaggio all’utente
        tg_send(chat_id, "🎉 Benvenuto! Torna sul sito per completare la registrazione.")

        # Messaggio all’owner
        if OWNER_CHAT_ID:
            tg_send(
                OWNER_CHAT_ID,
                f"📢 Nuovo utente con codice promo {promo}!\nChat ID: {chat_id}"
            )

        # Non possiamo fare redirect dal webhook Telegram,
        # ma la logica lato web è: quando l’utente ritorna sul sito e il promo code è stato usato,
        # lo rimandiamo automaticamente a /register/<promo>
        return "ok"

    return "ignored"
