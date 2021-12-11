from __init__ import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from sqlalchemy.sql import func
from wtforms import SelectField

# will be updated with workitem schema
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    status = db.Column(db.String(20), default="PENDING")
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # foreign keys are lower case

    def __repr__(self):
        # returns the name of recod Need to determine what to return 
        # return f'Note {self.PLACEHOLDER}'
        pass

class Form(FlaskForm):
    status = SelectField('status', choices=WI_STATUS, default="")
    
# user database table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship("Note") # relational reference are capital
    