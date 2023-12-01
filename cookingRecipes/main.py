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
    ingredientsAlr = db.session.execute(query_ingredients).all()
    query = (
        db.select(model.Ingredients.ingredient)
        .order_by(model.Ingredients.ingredient.desc())
    )
    ingredients = db.session.execute(query).all()
    ingredients_list = [item[0] for item in ingredients]
    ingredients_string = ', '.join(ingredients_list)
    query_images = (
         db.select(model.Photos.img)
         .where(model.Photos.recipe_id == recipe.id)
    )
    photos = db.session.execute(query_images).scalars().all()
    image = base64.b64encode(recipe.img).decode("utf-8")
    imgObj = {"image": image}
    return render_template("main/editRecipe.html", recipe=recipe, steps=steps, ingredientsAlr=ingredientsAlr, photos=photos, imgObj=imgObj, ingredients=ingredients_string)

#TODO: FINISH
@bp.route("/updateRecipe", methods=["POST"])
@flask_login.login_required
def updateRecipe():
    print(request.form)
    recipe_id = request.form.get("recipe_id")
    recipe = db.session.get(model.Recipe, recipe_id)
    #update num_people, cooking_time, steps, img and ingredients IF DIFFERENT
    title = request.form.get("title")
    description = request.form.get("description")
    cooking_time = request.form.get("cooking_time")
    num_people = request.form.get("num_people")
    img_data = request.form.get("imgData")
    if img_data and img_data != '':
        decoded = base64.b64decode(img_data)
        if decoded != recipe.img:
            recipe.img = decoded
    quantified_ingredients_list = json.loads(request.form.get("quantified_ingredients"))
    ingredients_list = json.loads(request.form.get("ingredientsNew"))
    oldQuants = json.loads(request.form.get("oldQuants"))
    oldIngrs = json.loads(request.form.get("oldIngrs"))
    steps = json.loads(request.form.get("steps"))
    if recipe.title != title:
        recipe.title = title
    if recipe.description != description:
        recipe.description = description
    if recipe.cooking_time != cooking_time:
        recipe.cooking_time = cooking_time
    if recipe.num_people != num_people:
        recipe.num_people = num_people
    query_alrSteps = (
        db.select(model.Steps)
        .where(model.Steps.recipe_id == recipe_id)
        .order_by(model.Steps.sequence_num.desc())
    )
    alrSteps = db.session.execute(query_alrSteps).scalars().all()
    for i in range(len(steps)):
        if (i >= len(alrSteps)):
            break
        if alrSteps[i].description != steps[i]:
            alrSteps[i].description = steps[i]
    if (len(steps) > len(alrSteps)):
        for i in range(len(alrSteps), len(steps)):
            newStep = model.Steps(
                recipe_id=recipe_id, sequence_num=i+1,
                description=steps[i]
            )
            db.session.add(newStep)
    else:
        #deleting all old steps that aren't in new steps
        for i in range(len(steps), len(alrSteps)):
            db.session.delete(alrSteps[i])
    query_ingr = (
        db.select(model.QuantifiedIngredients.id, model.QuantifiedIngredients.quantity, model.Ingredients.ingredient, model.QuantifiedIngredients.ingredient_id)
        .join(model.Ingredients, model.QuantifiedIngredients.ingredient_id == model.Ingredients.id)
        .where(model.QuantifiedIngredients.recipe_id == recipe_id)
    )
    prevQuantsAndIngrs = db.session.execute(query_ingr).all()
    for prev in prevQuantsAndIngrs:
        if prev.ingredient in oldIngrs:
            i = oldIngrs.index(prev.ingredient)
            if prev.quantity != oldQuants[i]:
                prev.quantiy = oldQuants[i]
        else:
            db.session.delete(db.session.get(model.QuantifiedIngredients, prev.id))
            db.session.flush()
            query_any = (
                db.select(model.QuantifiedIngredients)
                .where(model.QuantifiedIngredients.ingredient_id == prev.ingredient_id)
            )
            if db.session.execute(query_any).first() is None:
                ingr = db.session.get(model.Ingredients, prev.ingredient_id)
                db.session.delete(ingr)
                db.session.flush()
    for i in range(len(quantified_ingredients_list)):
        try:
            ingredient = db.session.query(model.Ingredients).filter(model.Ingredients.ingredient==ingredients_list[i]).one()
        except NoResultFound:
            ingredient = model.Ingredients(ingredient=ingredients_list[i])
            db.session.add(ingredient)
            db.session.flush()
        newQuantIngredient = model.QuantifiedIngredients(
            recipe_id=recipe_id, ingredient_id=ingredient.id, quantity=quantified_ingredients_list[i]
        )
        db.session.add(newQuantIngredient)
    db.session.commit()
    return {"recipe_id": recipe_id}


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
