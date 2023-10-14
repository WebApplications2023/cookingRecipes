import datetime
import dateutil.tz

from flask import Blueprint, render_template
import flask_login


from . import model

bp = Blueprint("main", __name__)


@bp.route("/")
@flask_login.login_required
def index():

    img_sophia = open('./microblog/static/resources/sophia.png', 'rb').read()
    img_maeve = open('./microblog/static/resources/maeve.png', 'rb').read()
    img_kate = open('./microblog/static/resources/kate.png', 'rb').read()
    
    user = model.User(email = "sophia@example.com", name = "Sophia Weiler", handle = "sophiaweiler", img = img_sophia, password = "123")
    user2 = model.User(email = "maeve@example.com", name = "Maeve Balavender", handle = "maeveb", img = img_maeve, password = "123")
    user3 = model.User(email = "kate@example.com", name = "Kate Roth", handle = "kroth", img = img_kate, password = "123")

    posts = [
        model.Message(
            user = user2, 
            text = "So happy to be done with school for today.", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            user = user, 
            text = "Just working on my Web Applications homework!!!",
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            user = user3, 
            text = "Finally made it back to Cork :)",
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            user = user, 
            text = "Oktoberfest is so much fun!", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            user = user2, 
            text = "What should I pack for this weekend?", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            user = user3, 
            text = "Getting SOOOO excited to see everyone!!!!",
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
    ]
    
    return render_template("main/index.html", posts=posts, user=user)


@bp.route("/profile")
@flask_login.login_required
def profile():
    return render_template("main/profile.html")

"""
@bp.route("/postResponse")
@flask_login.login_required
def postResponse():
    user = model.User("soph@example.com", "Sophia Weiler", "sophiaweiler", "sophia.png")
    user2 = model.User("maeve@example.com", "Maeve Balavender", "maeveb", "maeve.png")
    user3 = model.User("kate@example.com", "Kate Roth", "kroth", "kate.png")
    posts = [
        model.Message(
            user = user, 
            text = "Just working on my Web Applications homework!!!", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
    ]
    responses = [
        model.Message(
            user = user3, 
            text = "CS Queen slay", 
            timestamp = datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            2, user2, "Let's go to the cafe soon!", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
    ]
    return render_template("main/postResponse.html", posts=posts, user=user, responses=responses)
"""
