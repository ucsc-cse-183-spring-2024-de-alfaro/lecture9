"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

db.define_table('bird',
    Field('species'),
    Field('number', 'integer', requires = IS_INT_IN_RANGE(0, 1000)),
    Field('heard', 'integer', requires = IS_INT_IN_RANGE(0, 1000)),
    Field('created_on', 'datetime', default=get_time),
    Field('created_by', default=get_user_email),
)

db.bird.created_on.readable = db.bird.created_on.writable = False
db.bird.created_by.readable = db.bird.created_by.writable = False

db.commit()
