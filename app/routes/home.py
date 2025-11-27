@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        promo = PromoCode.query.filter_by(code=code).first()

        if not promo:
            flash("❌ Codice non valido.")
            return redirect(url_for("home"))

        # Se il promo è già stato collegato ad un chat_id → redirect automatico alla registrazione
        if promo.redeemed and promo.assigned_user_id:
            return redirect(url_for("register", promo=promo.code))

        return redirect(url_for("register", promo=promo.code))

    return render_template("index.html", bot_username=BOT_USERNAME)
