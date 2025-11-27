from flask import Blueprint, render_template, request, redirect, url_for, current_app
from ..models import PromoCode, User
from .. import db

register_bp = Blueprint("register", __name__)

@register_bp.route("/register/<promo>", methods=["GET", "POST"])
def register_user(promo):
    promo_row = PromoCode.query.filter_by(code=promo).first_or_404()
    user = User.query.get(promo_row.assigned_user_id) if promo_row.assigned_user_id else None

    if request.method == "POST":
        name = request.form.get("name")
        if user:
            user.name = name
        else:
            user = User(name=name, promo_code=promo)
            db.session.add(user)
            promo_row.assigned_user_id = user.id

        promo_row.redeemed = True
        db.session.commit()

        return redirect(url_for("booking.booking_page", user_id=user.id))

    return render_template("registration.html",
                           promo=promo,
                           user=user,
                           bot_username=current_app.config["TELEGRAM_BOT_USERNAME"])
