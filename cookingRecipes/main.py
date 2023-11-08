import datetime
import dateutil.tz

from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
import flask_login


from . import model, db

bp = Blueprint("main", __name__)


@bp.route("/")
def index():

    """followers = db.aliased(model.User)
    query = (
        db.select(model.Message)
        .join(model.User)
        .join(followers, model.User.followers)
        .where(followers.id == flask_login.current_user.id)
        .where(model.Message.response_to == None)
        .order_by(model.Message.timestamp.desc())
        .limit(10)
    )
    posts = db.session.execute(query).scalars().all()
    """
    return render_template("main/index.html")

#SAVE FOR VIEWING ONE RECIPE
@bp.route("/post/<int:messageID>")
@flask_login.login_required
def post(messageID):
    message = db.session.get(model.Message, messageID)
    if not message:
        abort(404, "Post id {} doesn't exist.".format(messageID))
    if message.response_to:
        abort(403, "You can not view a response message in this form")
    
    query = db.select(model.Message).where(model.Message.response_to == message).order_by(model.Message.timestamp.desc())
    responses = db.session.execute(query).scalars().all()
    return render_template("main/postResponse.html", posts=[message], responses = responses)

#SAVE FOR PROFILE PATH
@bp.route("/profile/<int:userID>")
@flask_login.login_required
def profile(userID):
    userQuery = db.select(model.User).where(model.User.id == userID)
    user = db.session.execute(userQuery).scalar()
    query = db.select(model.Message).where(model.Message.user_id == userID).where(model.Message.response_to == None).order_by(model.Message.timestamp.desc())
    posts = db.session.execute(query).scalars().all()

    if user is not None:
        numFollowers = len(user.followers)
        numFollowing = len(user.following)
    else:
        numFollowers = 0
        numFollowing = 0
    
    
    if userID == flask_login.current_user.id:
        following = "none"
    elif user in flask_login.current_user.following:
        following = "unfollow"
    else:
        following = "follow"

    return render_template("main/profile.html", posts=posts, user=user, followButton = following, numFollowers=numFollowers, numFollowing=numFollowing )

#SAVE FOR NEW RECIPE
@bp.route("/newPost")
@flask_login.login_required
def renderPost():
    return render_template("main/post.html")


#SAVE FOR NEW RECIPE
@bp.route("/newPost", methods=["POST"])
@flask_login.login_required
def newPost():
    text = request.form.get("text")
    user = flask_login.current_user
    time = datetime.datetime.now()
    responseTo = request.form.get("response_to")

    
    if responseTo:
        message = db.session.get(model.Message, responseTo)
        #messageQuery = db.select(model.Message).where(model.Message.id == responseTo)
        #message = db.session.execute(messageQuery).scalar()
        if message is None:
            abort(404, "Post id {} doesn't exist.".format(responseTo))
    else:
        message = None
        
    
    newMessage = model.Message(user=user, text=text, timestamp=time, response_to = message)
    db.session.add(newMessage)
    db.session.commit()


    query = db.select(model.Message).where(model.Message.response_to == message).order_by(model.Message.timestamp.desc())
    responses = db.session.execute(query).scalars().all()
    
    if responseTo:
        return render_template("main/postResponse.html", posts=[message], responses=responses)
    
    return redirect(url_for("main.index"))




