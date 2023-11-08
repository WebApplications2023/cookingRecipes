import datetime
import dateutil.tz

from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
import flask_login


from . import model, db

bp = Blueprint("main", __name__)


@bp.route("/")
@flask_login.login_required
def index():

    followers = db.aliased(model.User)
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

    return render_template("main/index.html", posts=posts)

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

@bp.route("/newPost")
@flask_login.login_required
def renderPost():
    return render_template("main/post.html")

@bp.route("/postReply/<int:postId>")
@flask_login.login_required
def postReply(postId):
    return render_template("main/postReply.html", id=postId)

@bp.route("/postResponse")
@flask_login.login_required
def postResponse():
    return render_template("main/postResponse.html")


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

@bp.route("/follow/<int:userID>", methods=["POST"])
@flask_login.login_required
def follow(userID):
    #get user from the db
    userQuery = db.select(model.User).where(model.User.id == userID)
    user = db.session.execute(userQuery).scalar()
    
    if user is None:
        abort(404, "User id {} doesn't exist.".format(userID))
    #check that they aren't the same user
    if flask_login.current_user.id == userID:
        abort(403, "You can't follow yourself.")
    #check that they don't already follow them
    if flask_login.current_user in user.followers:
        abort(403, "You already follow them")
    else:
        user.followers.append(flask_login.current_user)
        db.session.commit()
    
    return redirect(url_for("main.profile", userID = user.id))

@bp.route("/unfollow/<int:userID>", methods=["POST"])
@flask_login.login_required
def unfollow(userID):
    #get user from the db
    userQuery = db.select(model.User).where(model.User.id == userID)
    user = db.session.execute(userQuery).scalar()

    if not user:
        abort(404, "User id {} doesn't exist.".format(userID))
    #check that they aren't the same user
    if flask_login.current_user.id == userID:
        abort(403, "You can't follow yourself.")
    #check that they don't already follow them
    if flask_login.current_user not in user.followers:
        abort(403, "You don't already follow them")
    else:
        user.followers.remove(flask_login.current_user)
        db.session.commit()
    
    return redirect(url_for("main.profile", userID = user.id))

@bp.route("/profile/<int:userID>/<string:follow>")
@flask_login.login_required
def listFollow(userID, follow):
    userQuery = db.select(model.User).where(model.User.id == userID)
    user = db.session.execute(userQuery).scalar()

    if not user:
        abort(404, "User id {} doesn't exist.".format(userID))
    
    if follow == "following":
        follows = user.following
        followType = "Following"
    elif follow == "followers":
        follows = user.followers
        followType = "Followers"
    else:
        abort(404, "Not a valid command")
    