from __init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# will be updated with workitem schema
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_coordinate = db.Column(db.Float, default=None)
    y_coordinate = db.Column(db.Float, default=None)
    state = db.Column(db.String(50), default=None)
    city = db.Column(db.String(150), default=None)
    location = db.Column(db.String(150), default=None)
    customer_name = db.Column(db.String(1000), default=None)
    product = db.Column(db.String(100), default=None)
    units = db.Column(db.Integer, default=None)
    price = db.Column(db.Float, default=None)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # foreign keys are lower case
    route_id = db.Column(db.Integer, db.ForeignKey("route.id"))


# user database table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    notes = db.relationship("Note")  # relational reference are capital


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shortest_full_path = db.Column(db.String(2000), default=None)
    display_shortest_full_path = db.Column(db.String(2000), default=None)
    shortest_full_path_value = db.Column(db.Float, default=None)
    altered_path = db.Column(db.String(2000), default=None)
    display_altered_path = db.Column(db.String(2000), default=None)
    altered_path_value = db.Column(db.Float, default=None)
    status = db.Column(db.String(30), default="PENDING")
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    alternate_route = db.Column(db.Boolean, default=False)
