from database import db
from datetime import datetime
import uuid

class PassbookModel(db.Model):
    __tablename__ = "passbooks"

    id = db.Column(db.String, primary_key=True,default=lambda: uuid.uuid4().hex)
    payer_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    payee_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    expense_id = db.Column(db.String, db.ForeignKey("expenses.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
    expense = db.relationship("ExpenseModel", back_populates="passbook_entries")
    payer = db.relationship("UserModel", foreign_keys=[payer_id], back_populates="passbook_for_payer")
    payee = db.relationship("UserModel", foreign_keys=[payee_id], back_populates="passbook_for_payee")
