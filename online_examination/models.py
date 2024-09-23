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
    role = db.Column(db.String(20), nullable=False) #role will be admin or student

    
    def __repr__(self):
        return f"User('{self.email}', '{self.firstName}')"

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='exam', cascade="all, delete-orphan", lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(300), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id', ondelete="CASCADE"), nullable=False)
    choices = db.relationship('Choice', backref='question', cascade="all, delete-orphan", lazy=True)
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete="CASCADE"), nullable=False)

class StudentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    score = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # e.g., "Pass" or "Fail"

with app.app_context():
    db.create_all()
