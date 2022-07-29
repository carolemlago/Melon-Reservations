"""CRUD operations."""

from model import Reservation, db, User, connect_to_db


# Functions start here!

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

# Create user
def create_user(email, hashed):
    """Create and return a new user."""

    user = User(email=email, hashed=hashed)

    return user

# Create reservation
def create_reservation(user_id, start_time, end_time):

    """ Create and return new reservation """
    
    
    reservation = Reservation(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time
    )

    return reservation

# Functions to query database
def get_reservations():
    """Return all reservations."""
    return Reservation.query.all()

def get_reservations_by_date(date):
    """Return all reservations of a specific date."""
    return Reservation.query.filter_by(date).all()


def get_reservations_by_start_time(date, start_time):
    """Return all reservations of a specific time."""
    return Reservation.query.filter(date == date, start_time=start_time).all()

def get_reservation_by_id(reservation_id):
    """Get reservation by its id"""
    return Reservation.query.get(reservation_id)

def get_user_by_id(user_id):
    """Get user by its id"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email"""    
    return User.query.filter(User.email == email).first()

def get_reservations_by_user_id(user_id):
    """ Return user's reservations by it's id"""
    return Reservation.query.filter(User.user_id == user_id).all()

def delete_reservation(reservation_id):
    """Delete selected reservation."""
    deleted_reservation = Reservation.query.get(reservation_id)

    db.session.delete(deleted_reservation)
    db.session.commit()