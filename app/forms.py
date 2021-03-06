from flask_wtf import Form
# from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, IntegerField, SelectField, SelectMultipleField, BooleanField, validators
# from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Email, Length
from wtforms.fields.html5 import DateField
# from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField

from .models import Volunteer

class VolunteerForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    role = SelectField('Role', choices = [('open-hours', 'open-hours'), ('shopper','shoppers'), ('both', 'both')] )

class OpenhourForm(Form):
    date = DateField('Date', format='%Y-%m-%d')
    volunteers = SelectMultipleField('Volunteers', coerce=int)
    shoppers = SelectMultipleField('Shoppers', coerce=int)

class NoteForm(Form):
    author = SelectField('Name', coerce=int)
    customers = IntegerField('Number of Customers')
    body = TextAreaField('Notes')
    shopping = TextAreaField('Shopping List', [validators.DataRequired()])

class UserForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=50)])
    password = StringField('Password', [validators.DataRequired()])

class ReminderEmailForm(Form):
    start_time = StringField('Start Time', [validators.DataRequired()])
    door_code = StringField('Door Code', [validators.DataRequired()])
    pantry_code = StringField('Pantry Code', [validators.DataRequired()])

class SignupForm(Form):
    volunteer = SelectField('Name', coerce=int)

class EmailForm(Form):
    send_date = DateField('Send Date', format='%Y-%m-%d')
    recipients = StringField('To: ')
    subject = StringField('Subject: ')
    message = TextAreaField('Body')
