from marshmallow import Schema, fields, validates, ValidationError
from models import ExpenseType
from datetime import datetime
import math
import re

class UserSchema(Schema):

    id = fields.Str()
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    mobile_number = fields.Int(required=True)

    @validates('mobile_number')
    def validate_mobile(self, mobile_number):
        if mobile_number < 6000000000 or mobile_number > 9999999999:
            raise ValidationError('Mobile number should be valid')
    
    @validates('email')
    def validate_email(self, email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex,email)):
            raise ValidationError('Email is not valid')


class UserPassbookSchema(Schema):
    
    user_role = fields.String()
    user_id = fields.String()
    amount = fields.Float()
    expense_name = fields.String()
    expense_type = fields.String()


class ExpenseSchema(Schema):

    id = fields.Str(dump_only=True)
    expense_name = fields.Str(required=True)
    payer_id = fields.Str(required=True)
    date = fields.DateTime(default=datetime.now())
    amount = fields.Float(required=True)
    expense_type = fields.Enum(ExpenseType, required=True)
    user_ids = fields.Dict(keys=fields.Str(), values=fields.Float(), required=True)

    @validates('user_ids')
    def validate_user_ids(self, user_ids):
        if len(user_ids) > 1000:
            raise ValidationError('Each expense can have up to 1000 participants.')

    @validates('amount')
    def validate_amount(self, amount):
        if amount > 10000000:
            raise ValidationError('The maximum amount for an expense can go up to INR 1,00,00,000/')
        
        if not math.isclose(amount, round(amount, 2), abs_tol=0.01):
            raise ValidationError('Amount should have up to two decimal places.')
