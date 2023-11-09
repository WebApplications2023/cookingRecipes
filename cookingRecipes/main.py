import datetime
import dateutil.tz

from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
import flask_login

from . import model, db

bp = Blueprint("main", __name__)

#HOMEPAGE
@bp.route("/")
def index():
    query = (
        db.select(model.Recipes)
        .order_by(model.Message.timestamp.desc())
        .limit(10)
    )
    recipes = db.session.execute(query).scalars().all()
    return render_template("main/index.html", recipes=recipes)

#SAVE FOR VIEWING ONE RECIPE
@bp.route("/recipe/<int:recipe_id>")
@flask_login.login_required
def recipe(recipe_id):
    recipe = db.session.get(model.Recipe, recipe_id)
    if not recipe:
        abort(404, "Recipe id {} doesn't exist.".format(recipe_id))
    if recipe.response_to:
        abort(403, "You can not view a response message in this form")
    return render_template("main/recipeCard_template.html", recipe=recipe)


#SAVE FOR PROFILE PATH
@bp.route("/profile/<int:userID>")
@flask_login.login_required
def profile(userID):
    userQuery = db.select(model.User).where(model.User.id == userID)
    user = db.session.execute(userQuery).scalar()
    query = (
        db.select(model.Recipes)
        .where(model.Recipes.user_id == userID)
        .order_by(model.Message.timestamp.desc())
        .limit(10)
    )
    recipes = db.session.execute(query).scalars().all()

    #USE IF IMPLEMENTING FOLLOW FEATURE
    # if user is not None:
    #     numFollowers = len(user.followers)
    #     numFollowing = len(user.following)
    # else:
    #     numFollowers = 0
    #     numFollowing = 0
    
    
    # if userID == flask_login.current_user.id:
    #     following = "none"
    # elif user in flask_login.current_user.following:
    #     following = "unfollow"
    # else:
    #     following = "follow"

    return render_template("main/profile.html", recipes=recipes )

#SAVE FOR NEW RECIPE
# @bp.route("/newPost")
# @flask_login.login_required
# def renderPost():
#     return render_template("main/post.html")


#SAVE FOR NEW RECIPE
@bp.route("/newRecipe", methods=["POST"])
@flask_login.login_required
def newPost():
    title = request.form.get("text")
    user = flask_login.current_user
    description = request.form.get("description")
    num_people = request.form.get("num_people")
    cooking_time = request.form.get("cooking_time")
    img = request.form.get("img")
    steps = request.form.get("steps") #need to figure out to format these to seperate steps
    # ingredients will be dropdown menu, will have to be the same 
    # length as quantified ingredients
    quantified_ingredients = request.form.get("quantified_ingredients")
    ingredients = request.form.get("ingredients")

    newRecipe = model.Message(
        title=title, user=user, description=description, 
        num_people=num_people, cooking_time=cooking_time, img=img, 
        steps=steps, quantified_ingredients=quantified_ingredients,
        ingredients=ingredients
    )
    db.session.add(newRecipe)
    db.session.commit()

    return redirect(url_for("main.index"))

