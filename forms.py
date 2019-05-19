from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class AddHW(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category = StringField("Category")
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RemoveHW(FlaskForm):
    pass

class UpdateHW(FlaskForm):
    pass

class Checkout(FlaskForm):
    outdate = DateField("Date", validators=[DataRequired()])
    whom = StringField("Who", validators=[DataRequired()])
    #what =
    reason = StringField("Reason")
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    #authorized =

class Checkin(FlaskForm):
    pass

