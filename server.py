"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from urllib.parse import _ResultMixinStr
from passlib.hash import argon2
from pprint import pformat
import os
import requests
import time
import datetime

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def log_in():

    """ Show log in page """
    return render_template("login.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    """ Create new user """

    email = request.form.get("email")
    user_password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    
    # Hashing password
    hashed = argon2.hash(user_password)
    
    del user_password

    user = crud.get_user_by_email(email)

    # Check if user already have an account
    if user:
        flash("User email already exists.")
        return redirect("/login")

    elif not argon2.verify(confirm_password, hashed):
        flash("Passwords don't match. Try again.")

    # Create new user in the database with user's info from the html form
    else:
        user = crud.create_user(email, hashed)
        db.session.add(user)    
        db.session.commit()
        user_id = user.user_id
        flash('Account created!')
        session['user_id'] = user.user_id
        return redirect(f"/search_page")

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

@app.route('/results', methods=['POST'])
def show_results():
    """ Show results from search """

    # Data from search
    date = request.form.get("date")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")

    # Getting data from user in session
    user = crud.get_user_by_id(user_id=session['user_id'])

    # Check if time slot is available:
    time_availability = crud.get_reservations_by_start_time(date, start_time)
    if time_availability == None:

        # Create reservation
        reservation = crud.Reservation(user_id=user.user_id, start_time=start_time, end_time=end_time)
        db.session.add(reservation)
        db.session.commit()

    else:
        flash("There's no availability for this date and time")
        return redirect('/search_page')

    return render_template('booking_options.html', start_time=start_time, end_time=end_time, date=date, reservation=reservation, user=user)
       
@app.route('/reservations')
def all_reservations(user_id):
    """Display all reservations."""   

    if "user_id" in session:

        # Get user by id 
        user = crud.get_user_by_id(session['user_id'])
        reservations = crud.get_reservations_by_user_id(user.user_id)

    return render_template('reservations.html', reservations=reservations, user=user) 


@app.route('/delete_appointment', methods=['POST'])
def delete_time():
    """ Delete appointment from database """

    reservation_id = request.json.get("reservationId")
    
    crud.delete_reservation(reservation_id=reservation_id) 
    return ("Success!")

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)