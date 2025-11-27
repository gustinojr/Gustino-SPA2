from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import PromoCode, User

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        promo = PromoCode.query.filter_by(code=code).first()

        if not promo:
            flash("❌ Codice non valido.")
            return redirect(url_for("home.home"))

        if promo.redeemed and promo.assigned_user_id:
            return redirect(url_for("register.register", promo=promo.code))

        return redirect(url_for("register.register", promo=promo.code))

    return render_template("index.html")
