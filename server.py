"""Server for melon schedule app."""
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from datetime import datetime, timedelta
from dateutil.parser import parse
from model import Reservation, db, connect_to_db
import os

app = Flask(__name__)
app.secret_key = os.environ["APP_SECRET_KEY"]
connect_to_db(app)




@app.route("/")
def homepage():
    """View homepage."""

    return render_template("index.html")

@app.route("/logout")
def logout():
    """Logout and redirect homepage."""

    session.clear()

    return redirect("/")


@app.route("/reservations", methods=["POST", "GET"])
def get_user_reservations():
    """ Retrieve reservations the user has made."""
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
    else:
        # assign a value to username is user is in session
        if 'username' in session:
            username = session["username"]
        # if the user is not in session, redirect them to the homepage
        else:
            return redirect("/")
    existing_reservations = Reservation.retrieve_reservations(username)

    return render_template("reservations.html", reservations=existing_reservations)


@app.route('/search_page')
def show_user():
    """Show users dashboard."""

    # Check if user logged in
    if "user_id" in session:

        # Get user by id 
        user = crud.get_user_by_id(session['user_id'])

        # Get times for reservation
        date = request.args.get("date") 
        start_time = request.args.get("start_time") 
        end_time = request.args.get("end_time") 

    else:
        flash("You must be logged in to view user dashboard page")
        return redirect("/login")

    return render_template("search.html", user=user, date=date, start_time=start_time, end_time=end_time)

@app.route("/schedule")
def render_schedule():
    """ View scheduling page."""
    return render_template("schedule.html")
       
@app.route('/reservations')
def all_reservations(user_id):
    """Display all reservations."""   

    if "user_id" in session:

        # Get user by id 
        user = crud.get_user_by_id(session['user_id'])
        reservations = crud.get_reservations_by_user_id(user.user_id)

    return render_template('reservations.html', reservations=reservations, user=user) 

@app.route("/reservations/delete", methods=["POST"])
def delete_reservation():
    """ Delete reservations the user has made."""
    reservation_start = parse(request.json.get("startTime"))
    username = session["username"]

    reservation_to_delete = Reservation.find_reservation_by_start_and_user(
        reservation_start, username
    )
    db.session.delete(reservation_to_delete)
    db.session.commit()
    return "Success"

@app.route("/reservations/book", methods=["POST"])
def make_reservation():
    """ Create a reservation with the specified user and time."""
    reservation_start = parse(request.form.get("start_time"))
    username = session["username"]

    new_reservation = Reservation.create_reservation(username, reservation_start)
    db.session.add(new_reservation)
    db.session.commit()
    return redirect("/reservations")

@app.route("/search_reservations", methods=["GET"])
def search_reservation():
    start_time = parse(request.args.get("startTime"))
    end_time = parse(request.args.get("endTime"))

    available_times = Reservation.available_reservations(start_time, end_time, session["username"])
    return jsonify(available_times)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)