from database import db
from datetime import datetime
from enum import Enum

class ExpenseType(Enum):

    EQUAL = "EQUAL"
    EXACT = "EXACT"
    PERCENT = "PERCENT"

class ExpenseModel(db.Model):

    __tablename__ = "expenses"

    id = db.Column(db.String, primary_key=True)
    expense_name = db.Column(db.String, nullable=False)
    payer_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    payer = db.relationship("UserModel", back_populates="expenses")
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
    amount = db.Column(db.Float)
    expense_type = db.Column(db.Enum(ExpenseType))
    passbook_entries = db.relationship("PassbookModel", back_populates="expense")