from . import db
import flask_login


class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    recipes = db.relationship('Recipe', back_populates='user')
    """messages = db.relationship('Message', back_populates='user')
    following = db.relationship(
        "User",
        secondary=FollowingAssociation.__table__,
        primaryjoin=FollowingAssociation.follower_id == id,
        secondaryjoin=FollowingAssociation.followed_id == id,
        back_populates="followers",
    )
    followers = db.relationship(
        "User",
        secondary=FollowingAssociation.__table__,
        primaryjoin=FollowingAssociation.followed_id == id,
        secondaryjoin=FollowingAssociation.follower_id == id,
        back_populates="following",
    )

    


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='messages')
    text = db.Column(db.String(512), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)
    response_to_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    response_to = db.relationship('Message', back_populates='responses', remote_side=[id])
    responses = db.relationship('Message', back_populates='response_to', remote_side=[response_to_id])

    

class FollowingAssociation(db.Model):
    follower_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False
    )
    followed_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False
    )
      """
    
class Recipe(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512), nullable = False)
    user = db.relationship('User', back_populates='recipes')
    numPeople = db.Column(db.Integer, nullable=False)
    cookingTime = db.Column(db.Integer, nullable=False) #number of minutes
    img = db.Column(db.LargeBinary, nullable=False)

    