from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint("status", __name__)

@blp.route("/status")
class RegisterUser(MethodView):

    def get(self):
        return {"status":"ok"}