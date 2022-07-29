"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb reservations")
os.system('createdb reservations')
model.connect_to_db(server.app)
model.db.create_all()




for n in range(10):
    email = f'user{n}@test.com'  
    password = 'test'

    user = crud.create_user(email, password)
    model.db.session.add(user)

for _ in range(10):
    user_id = user_id
    start_time = start_time
    end_time = end_time

    reservation = crud.create_reservation(user_id, start_time, end_time)
    model.db.session.add(reservation)

model.db.session.commit()