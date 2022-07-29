"""Models for Wego Itinerary Planner app."""

from flask_sqlalchemy import SQLAlchemy
from passlib.hash import argon2
import datetime

db = SQLAlchemy()




def connect_to_db(flask_app, db_uri="postgresql:///reservations", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


class User(db.Model):
    """User's information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(25), nullable=False, unique=True)
    hashed = db.Column(db.String(100), nullable=False)  

    reservations = db.relationship("Reservation", back_populates="user")

    def __repr__(self):
        return f"<User user_id = {self.user_id} email = {self.email}>"


class Reservation(db.Model):
    """Reservation table"""

    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    date = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    

    user = db.relationship("User", back_populates="reservations")

   

    def __repr__(self):
        return f"<Reservation reservation_id = {self.reservation_id} date = {self.date} start_time = {self.start_time} end_time = {self.end_time} >"


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
