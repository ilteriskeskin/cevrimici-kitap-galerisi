from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    name = StringField('enter your name', validators=[DataRequired()])
    email = StringField('enter your email', validators=[DataRequired()])
    password_one = StringField('your password', validators=[DataRequired()])
    password_two = StringField('enter your password again', validators=[DataRequired()])
    avatar = StringField('enter your avatar', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField('enter your email', validators=[DataRequired()])
    password = StringField('enter your password', validators=[DataRequired()])

