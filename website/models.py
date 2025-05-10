# Our database models do not need methods
#pylint: disable=too-few-public-methods
'''Get database from website and user helper from flask'''
from flask_login import UserMixin
from website import db

# user_calendar_association_table = db.Table('user_calendar_association',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('calendar_id', db.Integer, db.ForeignKey('calendar.id'))
# )

class User(db.Model, UserMixin):
    '''User class that contains information for admin and students.'''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    events = db.relationship('Event', backref='calendar')

    # implement get_id method
    def get_id(self):
        return str(self.id)

class Event(db.Model):
    '''Event class that contains information for events.'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(120), nullable=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=True)
    all_day = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class DragAndDropEvent(db.Model):
    '''Drag and drop event class that contains information for drag and drop events.'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)