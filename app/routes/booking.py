from flask import Blueprint, request, redirect, url_for, flash, render_template
from datetime import datetime
from ..models import User, Reservation
from ..telegram import tg_send
from .. import db

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/booking/<int:user_id>", methods=["GET", "POST"])
def booking_page(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
        start = datetime.strptime(request.form.get("start_time"), "%H:%M").time()
        end = datetime.strptime(request.form.get("end_time"), "%H:%M").time()

        conflict = Reservation.query.filter(
            Reservation.date == date,
            Reservation.start_time < end,
            Reservation.end_time > start
        ).first()

        if conflict:
            flash("⚠ L'orario scelto non è disponibile.")
            return redirect(url_for("booking.booking_page", user_id=user.id))

        reservation = Reservation(
            user_id=user.id,
            date=date,
            start_time=start,
            end_time=end,
            service=request.form.get("service")
        )

        db.session.add(reservation)
        db.session.commit()

       # Invio messaggio all’utente
tg_send(
    user.chat_id,
    f"""Ciao {user.name},

Grazie per aver prenotato presso Gustino SPA!
La tua prenotazione è confermata per il {date.strftime('%d/%m/%Y')}
dalle {start_time.strftime('%H:%M')} alle {end_time.strftime('%H:%M')}.

A presto!"""
)

# Invio messaggio all’owner
if OWNER_CHAT_ID:
    tg_send(
        OWNER_CHAT_ID,
        f"📢 Nuova prenotazione!\nUtente: {user.name}\nData: {date}\nOrario: {start_time}-{end_time}"
    )

        flash("Prenotazione completata!")
        return redirect(url_for("booking.booking_page", user_id=user.id))

    return render_template("booking.html", user=user)
