from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password_one = StringField('password', validators=[DataRequired()])
    password_two = StringField('enter again password', validators=[DataRequired()])
    avatar = StringField('avatar', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

