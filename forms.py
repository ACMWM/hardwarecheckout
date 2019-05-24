from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, SubmitField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired, ValidationError

import auth


class AddHW(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category = StringField("Category", render_kw={"list": "categories"})
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_quantity(form, field):
        if field.data < 1:
            raise ValidationError("Must have at least one!")

class RemoveHW(FlaskForm):
    submit = SubmitField("Submit")
    delete = BooleanField("I want to delete ")
    def sethw(self, hw):
        self.hw = hw
        self.delete.label.text += hw.name

class UpdateHW(AddHW):
    def sethw(self, hw):
        self.hw = hw
        self.name.default = hw.name
        self.category.default = hw.category
        self.quantity.default = hw.quantity
        self.process()

class Checkout(FlaskForm):
    outdate = DateTimeField("Date", validators=[DataRequired()],
            default=datetime.now)
    who = StringField("Who", validators=[DataRequired()])
    reason = StringField("Reason")
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Checkout")

    def sethw(self, hw):
        self.hw = hw

    def validate_quantity(form, field):
        if field.data < 1:
            raise ValidationError("Must check out at least one!")
        elif field.data > form.hw.available:
            raise ValidationError("Only "+str(form.hw.available)+" available!")

class Return(FlaskForm):
    returndate = DateTimeField("Date", validators=[DataRequired()],
            default=datetime.now)
    confirm = BooleanField("I Confirm that ", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def setchk(self, chk):
        self.chk = chk
        self.confirm.label.text += (self.chk.hardware.name+" x"
                ""+str(self.chk.quantity)+" have been returned to the"
                " Hardware Lab.")

    def validate_returndate(form, field):
        if form.chk.outdate > field.data:
            raise ValidationError("Cannot Return Hardware before it was checked out!")

class NewUser(FlaskForm):
    email = StringField("Email")
    submit = SubmitField()

    def validate_email(form, field):
        field.data += "@"+auth.domain
        if auth.validemail(field.data) is None:
            raise ValidationError("Must be a valid email!")

class DelUser(FlaskForm):
    email = SelectField("User")
    submit = SubmitField()
