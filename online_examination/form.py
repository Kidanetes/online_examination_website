""" This module will contains classes which will be used for the html forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from online_examination.models import UserProfile
from flask_login import current_user

class SignUpForm(FlaskForm):
    """This class will define properties for the signup form
    Attributes
    """
    firstName = StringField('First name',
                            validators=[DataRequired(), Length(max=25)])
    lastName = StringField('Last name',
                           validators=[DataRequired(), Length(max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confrirm password', 
                                    validators=[DataRequired(),
                                    EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        """ This method will check if the email of the user is not
        used before to create another account"""
        user = UserProfile.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exist to another account')

class LoginForm(FlaskForm):
    """ This class will define properties for the login form"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class UpdatePassword(FlaskForm):
    """This class will define properties to change password"""
    old_password = PasswordField('old_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired()])
    confirm_new_password = PasswordField('confirm_new_password',
                                         validators=[DataRequired(),
                                                     EqualTo('new_password')])
    submit = SubmitField('Update')

    def validate_old_password(self, old_password):
        """validate if the user submitted correct password"""
        from online_examination import bcrypt
        if not bcrypt.check_password_hash(current_user.password, old_password.data):
            raise ValidationError('Enter the correct current password')

    def validate_new_password(self, new_password):
        """This is to check if the user enterd new password as the current password"""
        from online_examination import bcrypt
        if bcrypt.check_password_hash(current_user.password, new_password.data):
            raise ValidationError('This is your current password')

# Form to Add an Exam
class AddExamForm(FlaskForm):
    """ this is the format of a form to add new exam"""
    exam_name = StringField('Exam Name', validators=[DataRequired()])
    submit = SubmitField('Add Exam')

# Form to Delete an Exam
class DeleteExamForm(FlaskForm):
    """ this is the format of a form to delete an exam"""
    submit = SubmitField('Delete Exam')


# Form to Add a Question
class AddQuestionForm(FlaskForm):
    """ This is a format of a form to add questions with choices to a exam"""
    question_text = StringField('Question Text', validators=[DataRequired()])
    choice_1 = StringField('Choice 1', validators=[DataRequired()])
    choice_2 = StringField('Choice 2', validators=[DataRequired()])
    choice_3 = StringField('Choice 3', validators=[DataRequired()])
    choice_4 = StringField('Choice 4', validators=[DataRequired()])
    correct_choice = SelectField('Correct Choice', choices=[('1', 'Choice 1'), ('2', 'Choice 2'), ('3', 'Choice 3'), ('4', 'Choice 4')], validators=[DataRequired()])
    submit = SubmitField('Add Question')
