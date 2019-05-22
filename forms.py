from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SubmitField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired, ValidationError


class AddHW(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category = StringField("Category")
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RemoveHW(FlaskForm):
    submit = SubmitField("Submit")
    delete = BooleanField("I want to delete ")
    def sethw(self, hw):
        self.hw = hw
        self.delete.label.text += hw.name

class UpdateHW(FlaskForm):
    pass

class Checkout(FlaskForm):
    outdate = DateTimeField("Date", validators=[DataRequired()],
            default=datetime.now())
    who = StringField("Who", validators=[DataRequired()])
    #what =
    reason = StringField("Reason")
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    #authorized =
    submit = SubmitField("Checkout")

    def sethw(self, hw):
        self.hw = hw

    def validate_quantity(form, field):
        if field.data < 1:
            raise ValidationError("Must check out at least one!")
        elif field.data > form.hw.available:
            raise ValidationError("Only "+str(form.hw.available)+" available!")

class Checkin(FlaskForm):
    pass

