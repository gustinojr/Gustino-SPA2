from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from ..models import PromoCode

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET", "POST"])
def home():
    bot_username = current_app.config["TELEGRAM_BOT_USERNAME"]

    if request.method == "POST":
        code = request.form.get("code", "").strip()
        promo = PromoCode.query.filter_by(code=code).first()
        if not promo:
            flash("❌ Codice non valido.")
            return redirect(url_for("home.home"))

        return redirect(url_for("register.register_user", promo=promo.code))

    return render_template("index.html", bot_username=bot_username)
