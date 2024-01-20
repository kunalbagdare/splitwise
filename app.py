from flask import Flask
import settings
from flask_smorest import Api
from database import db
from resources.user import blp as UserBlueprint
from resources.status import blp as StatusBlueprint
from resources.expense import blp as ExpenseBlueprint
from resources.passbook import blp as PassbookBlueprint


def create_app():
    """
    The `create_app` function creates and configures a Flask application with various settings and
    blueprints for different routes.
    """

    app = Flask(__name__)

    app.config["API_TITLE"] = "MY API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db" # local
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api = Api(app)

    # Initialize the database
    with app.app_context():
        db.create_all()

    # Register blueprints/routes
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(StatusBlueprint)
    api.register_blueprint(ExpenseBlueprint)
    api.register_blueprint(PassbookBlueprint)

    return app
