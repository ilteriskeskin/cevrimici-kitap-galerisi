from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from database import db
 
class User(object):
    def __init__(self, name, avatar, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.avatar = avatar
    def insert(self):
        if not db.find_one('user', {'email': self.email}):
            db.insert(collection='user', data=self.json())
    def json(self):
        return {
                "name": self.name,
                "avatar": self.avatar,
                "email": self.email,
                "password": self.password
                }
