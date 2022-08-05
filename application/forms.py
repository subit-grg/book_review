from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from datetime import date

class checkDateInFuture():
    def __init__(self, message):
        self.message = message
    
    def __call__(self, form, field):
        if field.data is None or field.data > date.today():
            raise ValidationError(self.message)

class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ReviewForm(FlaskForm):
    book = StringField('Book', validators=[DataRequired()])
    book_review = TextAreaField('Review', validators=[DataRequired()])
    review_date = DateField('Review Date', validators=[checkDateInFuture("Please choose a date in the future")])
    review_by = SelectField('Review by', choices=[])
    submit = SubmitField('Submit')