import datetime
import dateutil.tz

from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
import flask_login


from . import model, db

bp = Blueprint("main", __name__)


@bp.route("/")
@flask_login.login_required
def index():

    query = db.select(model.Message).order_by(model.Message.timestamp.desc()).limit(10)
    posts = db.session.execute(query).scalars().all()

    return render_template("main/index.html", posts=posts)

@bp.route("/post/<int:messageID>")
@flask_login.login_required
def post(messageID):
    message = db.session.get(model.Message, messageID)
    if not message:
        abort(404, "Post id {} doesn't exist.".format(messageID))
    return render_template("main/index.html", posts=[message])


@bp.route("/profile/<int:userID>")
@flask_login.login_required
def profile(userID):
    userQuery = db.select(model.User).where(model.User.id == userID)
    user = db.session.execute(userQuery).scalar()
    query = db.select(model.Message).where(model.Message.user_id == userID).order_by(model.Message.timestamp.desc())
    posts = db.session.execute(query).scalars().all()

    return render_template("main/profile.html", posts=posts, user=user)

@bp.route("/newPost")
@flask_login.login_required
def renderPost():
    return render_template("main/post.html")


@bp.route("/newPost", methods=["POST"])
@flask_login.login_required
def newPost():
    text = request.form.get("text")
    user = flask_login.current_user
    time = datetime.datetime.now()

    newMessage = model.Message(user=user, text=text, timestamp=time)
    db.session.add(newMessage)
    db.session.commit()

    return redirect(url_for("main.index"))

