from flask import Blueprint, render_template, request, redirect, url_for
from app.models import User, PromoCode
from app import db

register_bp = Blueprint("register", __name__, url_prefix="/register")

@register_bp.route("/<promo>", methods=["GET", "POST"])
def register(promo):
    promo_row = PromoCode.query.filter_by(code=promo).first_or_404()
    user = None

    if promo_row.assigned_user_id:
        user = User.query.get(promo_row.assigned_user_id)

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
        return redirect(url_for("booking.booking", user_id=user.id))

    return render_template("registration.html", promo=promo, user=user)
