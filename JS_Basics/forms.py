from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
import os
import bcrypt
from PIL import Image
from wtforms.validators import data_required, length, email, equal_to, ValidationError
class registration_form(FlaskForm):
    fname = StringField('Enter your First Name', validators=[data_required(), length(min=1, max= 30)])
    lname = StringField('Enter your Last Name', validators=[data_required(), length(min=1, max= 30)])
    username = StringField('Create a Username that meets the requirements', validators=[data_required(), length(min=8, max= 20)])
    email = StringField('Enter your Email. It must contain the @ sign (not verified)', validators=[data_required(), email()])
    password = StringField('Enter a Password', validators= [data_required(), length(min=8, max=20)])
    confirm_password = StringField('Confirm your Password', validators= [data_required(), length(min=8, max=20), equal_to('password')])
    submit = SubmitField('submit')



class login_form(FlaskForm):
    username = StringField('Enter Username', validators=[data_required(), length(min=2, max= 25)])
    password = StringField('Enter Password', validators= [data_required(), length(min=8, max=20)])
    rememberme = BooleanField('remember me')
    submit = SubmitField('login')