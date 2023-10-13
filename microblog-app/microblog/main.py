import datetime
import dateutil.tz

from flask import Blueprint, render_template


from . import model

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    user = model.User(1, "sophia@example.com", "Sophia Weiler", "sophiaweiler", "sophia.png")
    user2 = model.User(2, "maeve@example.com", "Maeve Balavender", "maeveb", "maeve.png")
    user3 = model.User(3, "kate@example.com", "Kate Roth", "kroth", "kate.png")

    posts = [
        model.Message(
            1, user2, "So happy to be done with school for today.", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            2, user, "Just working on my Web Applications homework!!!", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
         model.Message(
            3, user3, "Finally made it back to Cork :)", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            4, user, "Oktoberfest is so much fun!", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            4, user2, "What should I pack for this weekend?", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            4, user3, "Getting SOOOO excited to see everyone!!!!", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
    ]
    return render_template("main/index.html", posts=posts, user=user)

@bp.route("/profile")
def profile():
    user = model.User(2, "soph@example.com", "Sophia Weiler", "sophiaweiler", "sophia.png")
    posts = [
        model.Message(
            2, user, "Just working on my Web Applications homework!!!", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            4, user, "Oktoberfest is so much fun!", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
    ]
    return render_template("main/profile.html", posts=posts, user=user)

@bp.route("/postResponse")
def postResponse():
    user = model.User(2, "soph@example.com", "Sophia Weiler", "sophiaweiler", "sophia.png")
    user2 = model.User(2, "maeve@example.com", "Maeve Balavender", "maeveb", "maeve.png")
    user3 = model.User(3, "kate@example.com", "Kate Roth", "kroth", "kate.png")
    posts = [
        model.Message(
            2, user, "Just working on my Web Applications homework!!!", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
    ]
    responses = [
        model.Message(
            2, user3, "CS Queen slay", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
        model.Message(
            2, user2, "Let's go to the cafe soon!", datetime.datetime.now(dateutil.tz.tzlocal())
        ),
    ]
    return render_template("main/postResponse.html", posts=posts, user=user, responses=responses)