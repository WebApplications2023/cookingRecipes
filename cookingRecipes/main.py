import base64
import datetime
import json
import dateutil.tz
from werkzeug.utils import secure_filename 
from sqlalchemy.sql import func
from flask import Blueprint, abort, jsonify, render_template, request, redirect, url_for, flash
import flask_login
from sqlalchemy.orm.exc import NoResultFound

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
    return render_template("main/recipe.html")

#SAVE FOR VIEWING ONE RECIPE
@bp.route("/recipe/<int:recipeID>")
def recipe(recipeID):
    recipe = db.session.get(model.Recipe, recipeID)
    rating = db.session.query(func.avg(model.Ratings.rating)).filter(model.Ratings.recipe_id == recipeID).scalar()
    if not recipe:
        abort(404, "Recipe id {} doesn't exist.".format(recipeID))
    query_steps = (
        db.select(model.Steps.description)
        .where(model.Steps.recipe_id == recipe.id)
        .order_by(model.Steps.sequence_num)
    )
    steps = db.session.execute(query_steps).all()
    query_ingredients = (
        db.select(model.QuantifiedIngredients.quantity, model.Ingredients.ingredient)
        .join(model.Ingredients, model.QuantifiedIngredients.ingredients)
        .where(model.QuantifiedIngredients.recipe_id == recipeID)
    )
    ingredients = db.session.execute(query_ingredients).all()
    query_images = (
         db.select(model.Photos.img)
         .where(model.Photos.recipe_id == recipe.id)
     )
    photos = db.session.execute(query_images).scalars().all()
    if flask_login.current_user.is_authenticated:
        user = flask_login.current_user
        check = db.session.query(model.Bookmarks.id).filter(model.Bookmarks.recipe_id == recipeID).where(model.Bookmarks.user == user).first()
        bookmarked = True if check else False
    else:
        bookmarked = None
    return render_template("main/recipe.html", recipe=recipe, steps=steps, ingredients=ingredients, rating=rating, photos=photos, bookmarked=bookmarked)


#SAVE FOR PROFILE PATH
@bp.route("/profile/<int:userID>")
def profile(userID):
    user = db.session.get(model.User, userID)
    query = (
        db.select(model.Recipe)
        .where(model.Recipe.user_id == userID)
        .order_by(model.Recipe.timestamp.desc())
        .limit(10)
    )
    recipes = db.session.execute(query).scalars().all()
    query_submitted_photos = (
        db.select(model.Photos)
        .where(model.Photos.user_id == userID)
        .order_by(model.Photos.timestamp.desc())
    )
    submitted_photos = db.session.execute(query_submitted_photos).scalars().all()
    if flask_login.current_user == user:
        currUser = user
        query = (
            db.select(model.Recipe)
            .join(model.Bookmarks, model.Recipe.id == model.Bookmarks.recipe_id)
            .where(model.Bookmarks.user == user)
            .order_by(model.Recipe.timestamp)
        )
        bookmarks = db.session.execute(query).scalars().all() or None
    else:
        bookmarks = None
        currUser = None
    return render_template("main/profile.html", recipes=recipes, submitted_photos=submitted_photos, bookmarks=bookmarks, user=user, currUser=currUser)


@bp.route("/newRecipe")
@flask_login.login_required
def createRecipe():
    query = (
        db.select(model.Ingredients.ingredient)
        .order_by(model.Ingredients.ingredient.desc())
    )
    ingredients = db.session.execute(query).all()
    ingredients_list = [item[0] for item in ingredients]
    ingredients_string = ', '.join(ingredients_list)
    return render_template("main/recipeForm.html", ingredients=ingredients_string)


#SAVE FOR NEW RECIPE
@bp.route("/newRecipe", methods=["POST"])
@flask_login.login_required
def newRecipe():
    title = request.form.get("title") #TODO: update text identitiers to reflect frontend forms
    user = flask_login.current_user
    description = request.form.get("description")
    num_people = request.form.get("num_people")
    cooking_time = request.form.get("cooking_time")
    img = request.files["img"]  # Get the uploaded image file
    if img:
        # Ensure the image file has a safe filename
        img_filename = secure_filename(img.filename)
        img_data = img.read()  # Read the image data as binary
    else:
        img_data = None
    newRecipe = model.Recipe(
        title=title, user=user, description=description,
        num_people=num_people, cooking_time=cooking_time, img=img_data,
        timestamp=datetime.datetime.now(dateutil.tz.tzlocal())
    )

    db.session.add(newRecipe)
    db.session.commit() #should now be able to access newRecipe.id

    # ingredients will be dropdown menu, will have to be the same 
    # length as quantified ingredient
    quantified_ingredients_list = json.loads(request.form.get("quantified_ingredients"))
    ingredients_list = json.loads(request.form.get("ingredients"))

    for i in range(len(quantified_ingredients_list)):
        try:
            ingredient =  db.session.query(model.Ingredients).filter(model.Ingredients.ingredient==ingredients_list[i]).one()
        except NoResultFound:
            ingredient = model.Ingredients(ingredient=ingredients_list[i])
            db.session.add(ingredient)
            db.session.flush()
           
        newQuantIngredient = model.QuantifiedIngredients(
            recipe_id=newRecipe.id, ingredient_id = ingredient.id, quantity=quantified_ingredients_list[i]
        )
        db.session.add(newQuantIngredient)
        #TODO: need to check whether this also adds to recipe quantified ingredients list
        # or if I also need to append/if its better to just append
        #TODO: do I need a commit here?
    steps = json.loads(request.form.get("steps"))
    for i in range(len(steps)):
        newStep = model.Steps(
            recipe_id=newRecipe.id, sequence_num=i+1,
            description=steps[i]
        )
        db.session.add(newStep)
    db.session.commit()

    return redirect(url_for("main.recipe", recipeID=newRecipe.id))

@bp.route("/editRecipe", methods=["POST"])
@flask_login.login_required
def editRecipe():
    recipe_id = request.form.get("recipe_id")
    recipe = db.session.get(model.Recipe, recipe_id)
    rating = db.session.query(func.avg(model.Ratings.rating)).filter(model.Ratings.recipe_id == recipe_id).scalar()
    if not recipe:
        abort(404, "Recipe id {} doesn't exist.".format(recipe_id))
    query_steps = (
        db.select(model.Steps.description)
        .where(model.Steps.recipe_id == recipe.id)
        .order_by(model.Steps.sequence_num)
    )
    steps = db.session.execute(query_steps).all()
    query_ingredients = (
        db.select(model.QuantifiedIngredients.quantity, model.Ingredients.ingredient)
        .join(model.Ingredients, model.QuantifiedIngredients.ingredients)
        .where(model.QuantifiedIngredients.recipe_id == recipe_id)
    )
    ingredients = db.session.execute(query_ingredients).all()
    query_images = (
         db.select(model.Photos.img)
         .where(model.Photos.recipe_id == recipe.id)
     )
    photos = db.session.execute(query_images).scalars().all()
    if flask_login.current_user.is_authenticated:
        user = flask_login.current_user
        check = db.session.query(model.Bookmarks.id).filter(model.Bookmarks.recipe_id == recipe_id).where(model.Bookmarks.user == user).first()
        bookmarked = True if check else False
    else:
        bookmarked = None
    return render_template("main/editRecipe.html", recipe=recipe, steps=steps, ingredients=ingredients, rating=rating, photos=photos, bookmarked=bookmarked)


@bp.route("/addRating", methods=["POST"])
@flask_login.login_required
def addRating():
    rating = int(request.form.get("rating"))
    user = flask_login.current_user
    recipe_id = request.form.get("recipe_id")
    check = db.session.query(model.Ratings).filter(model.Ratings.recipe_id == recipe_id).filter(model.Ratings.user == user).first()
    if check is None:
        newRating = model.Ratings(rating=rating, user_id=user.id, recipe_id=recipe_id)
        db.session.add(newRating)
    else:
        check.rating = rating
    db.session.commit()
    return redirect(url_for("main.recipe", recipeID=recipe_id))
    #forward to recipe view

@bp.route("/addBookmark", methods=["POST"])
@flask_login.login_required
def addBookmark():
    user = flask_login.current_user
    recipe_id = request.form.get("recipe_id")
    check = db.session.query(model.Bookmarks.id).filter(model.Bookmarks.recipe_id == recipe_id).where(model.Bookmarks.user == user).first()
    if check is None:
        newBookmark = model.Bookmarks(recipe_id=recipe_id, user=user)
        db.session.add(newBookmark)
    else:
        delete = db.delete(model.Bookmarks).where(model.Bookmarks.recipe_id == recipe_id).where(model.Bookmarks.user == user)
        db.session.execute(delete)
    db.session.commit()
    return redirect(url_for('main.recipe', recipeID=recipe_id))


@bp.route("/addPhoto", methods=["POST"])
@flask_login.login_required
def addPhoto():
    img = request.files["img"]  # Get the uploaded image file
    user = flask_login.current_user
    recipe_id = request.form.get("recipe_id")
    if img:
        # Ensure the image file has a safe filename
        img_filename = secure_filename(img.filename)
        img_data = img.read()  # Read the image data as binary
        newPhoto = model.Photos(img=img_data, recipe_id=recipe_id, 
                                user_id=user.id, timestamp=datetime.datetime.now(dateutil.tz.tzlocal()))
        db.session.add(newPhoto)
        db.session.commit()
    else:
        flash("Please select a valid photo.")
    return redirect(url_for('main.recipe', recipeID=recipe_id))

@bp.route("/searchName", methods=["POST"])
def searchName():
    val = request.form.get("query")
    if val is not None and val != '':
        query_name = (
            db.select(model.Recipe.id, model.Recipe.title, model.Recipe.img)
            .distinct()
            .where(model.Recipe.title.contains(val))
        )
        search_name = db.session.execute(query_name).all()
        search_list = []
        for item in search_name:
            img = base64.b64encode(item.img).decode("utf-8")
            newObj = {"id": item.id, "title": item.title, "image": img}
            search_list.append(newObj)
        return search_list
    else:
        return None