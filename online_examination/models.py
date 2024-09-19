"""this module will contain UserProfile class which will define
model for SQLAlchemy"""


from online_examination import app, db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    """ This function will return the user using ID"""
    return UserProfile.query.get(id)


class UserProfile(db.Model, UserMixin):
    """This class will define the models for the UserProfile, which
    contians ID, firstName, lastName, email and Password"""
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(25), nullable=False)
    lastName = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"User('{self.email}', '{self.firstName}')"

with app.app_context():
    db.create_all()
