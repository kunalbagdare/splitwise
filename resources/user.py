from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import UserSchema
from models import UserModel
from database import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("users", __name__)


@blp.route("/add-user")
class AddUser(MethodView):

    @blp.arguments(UserSchema)
    @blp.response(201,UserSchema)
    def post(self, user_data):
        """
        The /add-user endpoint adds a new user to the database and returns the user object, handling potential
        errors along the way.
        """
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        
        except IntegrityError:
            abort(409, message="Email or mobile number already exists")

        except SQLAlchemyError:
            abort(500,message="Something went wrong in inserting user data")
        return user