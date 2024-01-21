from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import ExpenseSchema
from models import ExpenseModel, PassbookModel
from database import db
from scheduler.tasks import send_email
import math
import uuid
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("expenses", __name__)


@blp.route("/add-expense")
class AddExpense(MethodView):

    @blp.arguments(ExpenseSchema)
    @blp.response(201,ExpenseSchema)
    def post(self, expense_data):
        """
        The /add-expense endpoint takes in expense data, calculates individual shares based on the expense type, adds
        entries to the Passbook table, adds an expense entry to the Expense table, sends an
        email asynchronously, and returns the expense.
        """

        expense_type = expense_data['expense_type'].value
        try:
            expense_id = str(uuid.uuid4())
            if expense_type == 'PERCENT':
                percent_sum = sum(expense_data['user_ids'].values())
                if not math.isclose(percent_sum, 100, abs_tol=0.01):
                    abort(400, message="The total sum of percentage shares should be 100.")

                for user_id, percent_share in expense_data['user_ids'].items():
                    individual_share = round((percent_share / 100) * expense_data['amount'], 2)
                    
                    entry = PassbookModel(
                        payer_id=expense_data.get("payer_id"),
                        payee_id=user_id,
                        expense_id=expense_id,
                        amount=individual_share,
                    )
                    db.session.add(entry)
                

            elif expense_type == 'EXACT':
                sum_of_shares = sum(expense_data['user_ids'].values())
                if not math.isclose(sum_of_shares, expense_data['amount'], abs_tol=0.01):
                    abort(400, message="The total sum of shares should be equal to the total amount.")

                for user_id, share in expense_data['user_ids'].items():
                    entry = PassbookModel(
                        payer_id=expense_data.get("payer_id"),
                        payee_id=user_id,
                        expense_id=expense_id,
                        amount=share,
                    )
                    db.session.add(entry)

            elif expense_type == 'EQUAL':
                participants = len(expense_data['user_ids'])
                individual_share = round(expense_data['amount'] / participants, 2)

                for user_id in expense_data['user_ids']:

                    entry = PassbookModel(
                        payer_id=expense_data.get("payer_id"),
                        payee_id=user_id,
                        expense_id=expense_id,
                        amount=individual_share,
                    )
                    db.session.add(entry)


            expense_data["id"] = expense_id
            del expense_data["user_ids"]
            expense = ExpenseModel(**expense_data)
            db.session.add(expense)
            db.session.commit()

        
        except IntegrityError:
            abort(409, message="Email or mobile number already exists")

        except SQLAlchemyError:
            abort(500,message="Something went wrong in inserting user data")

        send_email.apply_async(args=[expense.id])
        return expense