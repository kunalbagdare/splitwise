from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify,request
from schema import UserPassbookSchema
from models import PassbookModel, ExpenseModel, UserModel
from utils import simplify_expenses

blp = Blueprint("passbook", __name__)


@blp.route("/expenses/<user_id>")
class UserExpenses(MethodView):

    @blp.response(200, UserPassbookSchema(many=True))
    def get(self, user_id):
        """
        The /expenses/<user_id> endpoint retrieves all entries from the PassbookModel for a given user, including both payer
        and payee entries, and returns them as a list of dictionaries.
        
        """

        payer_expense_ids = set(entry.expense_id for entry in PassbookModel.query.filter_by(payer_id=user_id).all())
        payee_entries = PassbookModel.query.filter_by(payee_id=user_id).all()

        all_entries = []

        for expense_id in payer_expense_ids:
            expense_entry = ExpenseModel.query.get_or_404(expense_id)
            if expense_entry:
                user_entry = {
                    "user_role": "payer",
                    "user_id": user_id,
                    "amount": expense_entry.amount,
                    "expense_name": expense_entry.expense_name,
                    "expense_type": expense_entry.expense_type.value
                }
                all_entries.append(user_entry)

        for entry in payee_entries:
            user_entry = {
                "user_role": "payee",
                "user_id": entry.payee_id,
                "amount": entry.amount,
                "expense_name": entry.expense.expense_name,
                "expense_type": entry.expense.expense_type.value
            }
            all_entries.append(user_entry)
        return all_entries



@blp.route("/balance/<user_id>")
class Balances(MethodView):

    @blp.response(200, dict)
    def get(self,user_id):
        """
        The /balance/<user_id> endpoint retrieves the balances of all users for a particular user excluding users with zero balances.

        """

        users = UserModel.query.all()

        all_user_balances = {}

        for user in users:
            if user.id == user_id:
                continue

            payer_expense_ids = set(entry.expense_id for entry in PassbookModel.query.filter_by(payer_id=user.id).all())
            payee_entries = PassbookModel.query.filter_by(payee_id=user.id).all()

            user_balance = 0.0

            for expense_id in payer_expense_ids:
                expense = ExpenseModel.query.get(expense_id)
                user_balance += expense.amount

            for entry in payee_entries:
                user_balance -= entry.amount

            if user_balance != 0:
                all_user_balances[user.name] = user_balance

        return jsonify(all_user_balances), 200


@blp.route("/balances")
class Balances(MethodView):

    @blp.response(200, dict)
    def get(self):
        """
        The /balances endpoint retrieves user balances and simplifies them if requested.
        """

        simplify = request.args.get('simplify', type=bool)

        users = UserModel.query.all()
        all_user_balances = {}

        for user in users:
            user_balance = 0.0

            payer_expense_ids = set(entry.expense_id for entry in PassbookModel.query.filter_by(payer_id=user.id).all())
            payee_entries = PassbookModel.query.filter_by(payee_id=user.id).all()

            for expense_id in payer_expense_ids:
                expense = ExpenseModel.query.get(expense_id)
                user_balance += expense.amount

            for entry in payee_entries:
                user_balance -= entry.amount
            
            # all_user_balances[user.id] = user_balance
            all_user_balances[user.name] = user_balance

        if simplify:
            simplified_balances = simplify_expenses(all_user_balances)
            return jsonify(simplified_balances), 200

        return jsonify(all_user_balances), 200




