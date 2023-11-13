import datetime
import dateutil.tz
from werkzeug.utils import secure_filename 
from sqlalchemy.sql import func
from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
import flask_login

from . import model, db

bp = Blueprint("main", __name__)

#HOMEPAGE
@bp.route("/")
def index():
    query = (
        db.select(model.Recipe)
        .order_by(model.Recipe.timestamp.desc())
        .limit(10)
    )
    recipes = db.session.execute(query).scalars().all()
    return render_template("main/index.html", recipes=recipes)

#TEMP
@bp.route("/recipe")
def example():
    return render_template("recipe.html")

#SAVE FOR VIEWING ONE RECIPE
@bp.route("/recipe/<int:recipeID>")
def recipe(recipeID):
    recipe = db.session.get(model.Recipe, recipeID)
    query = (
        db.select(model.Ratings.rating)
        .where(model.Ratings.recipe_id == recipeID)
    )
    if query:
        rating = db.session.execute(func.avg(query)) #TODO test once we have ratings in database
    else:
        rating = 0 #TODO change if we want to represent ratings in another way
    if not recipe:
        abort(404, "Recipe id {} doesn't exist.".format(recipeID))
    return render_template("main/recipeCard_template.html", recipe=recipe, rating=rating)


#SAVE FOR PROFILE PATH
@bp.route("/profile/<int:userID>")
@flask_login.login_required
def profile(userID):
    userQuery = db.select(model.User).where(model.User.id == userID)
    user = db.session.execute(userQuery).scalar()
    query = (
        db.select(model.Recipe)
        .where(model.Recipe.user_id == userID)
        .order_by(model.Recipe.timestamp.desc())
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
def newRecipe():
    title = request.form.get("text")
    user = flask_login.current_user
    description = request.form.get("description")
    num_people = request.form.get("num_people")
    cooking_time = request.form.get("cooking_time")
    img = request.files["img"]  # Get the uploaded image file
    if img:
        # Ensure the image file has a safe filename
        img_filename = secure_filename(img.filename)
        img_data = img.read()  # Read the image data as binary
    steps = request.form.get("steps") #need to figure out to format these to seperate steps
    # ingredients will be dropdown menu, will have to be the same 
    # length as quantified ingredients
    quantified_ingredients = request.form.get("quantified_ingredients")
    ingredients = request.form.get("ingredients")

    newRecipe = model.Recipe(
        title=title, user=user, description=description, 
        num_people=num_people, cooking_time=cooking_time, img=img_data, 
        steps=steps, quantified_ingredients=quantified_ingredients,
        ingredients=ingredients
    )
    db.session.add(newRecipe)
    db.session.commit()

    return redirect(url_for("main.index"))

@bp.route("/addRating", methods=["POST"])
@flask_login.login_required
def addRating():
    rating = request.form.get("rating")
    user = flask_login.current_user
    recipe_id = request.form.get("recipe_id") #hidden area of form?
    newRating = model.Rating(rating=rating, user_id=user.id, recipe_id=recipe_id)
    db.session.add(newRating)
    db.session.commit()
    return redirect("/recipe", recipeID=recipe_id) #TODO make sure this fits with view_recipe function
    #forward to recipe view