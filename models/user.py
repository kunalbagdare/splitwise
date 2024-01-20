from database import db
import uuid

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True,default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    mobile_number = db.Column(db.BigInteger,unique=True, nullable=False)
    expenses = db.relationship("ExpenseModel", back_populates="payer",lazy="dynamic")
    passbook_for_payer = db.relationship("PassbookModel", foreign_keys="PassbookModel.payer_id", back_populates="payer")
    passbook_for_payee = db.relationship("PassbookModel", foreign_keys="PassbookModel.payee_id", back_populates="payee")
