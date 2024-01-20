from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify,request
from schema import UserPassbookSchema
from models import PassbookModel, ExpenseModel, UserModel
# from database import db

blp = Blueprint("passbook", __name__)


@blp.route("/expenses/<user_id>")
class UserExpenses(MethodView):

    @blp.response(200, UserPassbookSchema(many=True))
    def get(self, user_id):

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



@blp.route("/balances")
class Balances(MethodView):

    @blp.response(200, dict)
    def get(self):

        simplify = request.args.get('simplify', type=bool)

        if simplify:
            all_user_balances = {}
            # TODO
            pass

        else:
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
                
                all_user_balances[user.id] = user_balance


        return jsonify(all_user_balances), 200