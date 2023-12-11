from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import base64

db = SQLAlchemy()
bcrypt = Bcrypt()



def create_app(test_config=None):
    app = Flask(__name__)


    # A secret for signing session cookies
    app.config["SECRET_KEY"] = "93220d9b340cf9a6c39bac99cce7daf220167498f91fa"
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://24_webapp_007:6YsJBKIo@mysql.lab.it.uc3m.es/24_webapp_007a"
    # Register blueprints
    # (we import main from here to avoid circular imports in the next lab)
    from . import main
    from . import auth

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from . import model

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(model.User, int(user_id))
    
    def base64_encode(blob_data):
        return base64.b64encode(blob_data).decode('utf-8')
    app.jinja_env.filters['base64_encode'] = base64_encode

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    db.init_app(app)
    return app


