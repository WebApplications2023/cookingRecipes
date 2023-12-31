from . import db
import flask_login


class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    recipes = db.relationship('Recipe', back_populates='user')
    ratings = db.relationship('Ratings', back_populates='user')
    bookmarks = db.relationship('Bookmarks', back_populates='user')
    photos = db.relationship('Photos', back_populates='user')


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='recipes')
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512), nullable = False)
    num_people = db.Column(db.Integer, nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False) #number of minutes
    img = db.Column(db.LargeBinary, nullable=False)
    steps = db.relationship('Steps', back_populates='recipe')
    quantified_ingredients = db.relationship('QuantifiedIngredients', back_populates='recipe')
    bookmarks = db.relationship('Bookmarks', back_populates='recipe')
    timestamp = db.Column(db.DateTime(), nullable=False)
    ratings = db.relationship('Ratings', back_populates='recipe')
    photos = db.relationship('Photos', back_populates='recipe')

class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe = db.relationship('Recipe', back_populates='steps')
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    sequence_num = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(512), nullable=False)

class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantified_ingredients = db.relationship('QuantifiedIngredients', back_populates='ingredients')
    ingredient = db.Column(db.String(64), nullable=False, unique=True)

class QuantifiedIngredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredients = db.relationship('Ingredients', back_populates='quantified_ingredients')
    recipe = db.relationship('Recipe', back_populates='quantified_ingredients')
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
    quantity = db.Column(db.String(64), nullable=False)


class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # 0 to 5 scale
    recipe = db.relationship('Recipe', back_populates='ratings')
    user = db.relationship('User', back_populates='ratings')

class Bookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='bookmarks')
    user = db.relationship('User', back_populates='bookmarks')

class Photos(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     img = db.Column(db.LargeBinary, nullable=False)
     recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
     recipe = db.relationship('Recipe', back_populates='photos')
     user = db.relationship('User', back_populates='photos')
     timestamp = db.Column(db.DateTime(), nullable=False)


