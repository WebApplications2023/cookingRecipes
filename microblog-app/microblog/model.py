"""class Message:
    def __init__(self, message_id, user, text, timestamp):
        self.message_id = message_id
        self.user = user
        self.text = text
        self.timestamp = timestamp


class User:
    def __init__(self, user_id, email, name, handle, img):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.handle = handle
        self.img = img
"""

from . import db
import flask_login

class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    handle = db.Column(db.String(64), nullable=False)
    img = db.Column(db.LargeBinary, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    messages = db.relationship('Message', back_populates='user')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='messages')
    text = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)
    response_to_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    response_to = db.relationship('Message', back_populates='responses', remote_side=[id])
    responses = db.relationship('Message', back_populates='response_to', remote_side=[response_to_id])
