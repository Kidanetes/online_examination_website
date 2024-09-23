"""this module will define routes to be used by the user"""


from flask import render_template, url_for, flash, redirect, request, session
from online_examination import app, db, bcrypt
from online_examination.form import SignUpForm, LoginForm, UpdatePassword,AddExamForm, DeleteExamForm, AddQuestionForm
from online_examination.models import UserProfile, Exam, StudentResult, Question, Choice
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home1():
    """return the home route"""
    return render_template('home.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    """return the login route, check if the user is not
    logged in, validate the correct information have been submitted,
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            user = UserProfile.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('home'))
            else:
                flash("wrong email or password", "success")
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """returns the signup route, check valid information have been submitted,
    the email have not been be used before"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = UserProfile(firstName=form.firstName.data,
                           lastName=form.lastName.data,
                           email=form.email.data,
                           password=hashed_password,
                           role="student")
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash("account created sucessfully", "success")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """logout the logged in user"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """ return the account of the logged in user,
    this route only works if the user is logged in"""
    form = UpdatePassword()
    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        db.session.commit()
        flash("password changed sucessfully", "success")
        return redirect(url_for('account'))
    return render_template('account.html', form=form)

@app.route('/about')
def about():
    """return the about page"""
    return render_template('about.html')


@app.route('/delete_exam', methods=['GET', 'POST'])
@login_required
def delete_exam():
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    exams = Exam.query.all()
    form = DeleteExamForm()
    return render_template('delete_exam.html', exams=exams, form=form)

@app.route('/delete_exam/<int:exam_id>', methods=['POST'])
@login_required
def delete_exam_action(exam_id):
  if current_user.role != 'admin':
      return redirect(url_for('home'))
  exam = Exam.query.get(exam_id)
  if exam:
      db.session.delete(exam)
      db.session.commit()                              
      flash('Exam deleted successfully!', 'success')
  return redirect(url_for('delete_exam'))

@app.route('/home')
@login_required
def home():
    if current_user.role == 'admin':
        return render_template('home1.html', is_admin=True)
    else:
        return redirect(url_for('exam_list'))

@app.route('/add_exam', methods=['GET', 'POST'])
@login_required
def add_exam():
    if current_user.role != 'admin':
        return redirect(url_for('home'))

    exams = Exam.query.all()
    form = AddExamForm()
    if form.validate_on_submit():
        new_exam = Exam(exam_name=form.exam_name.data)
        db.session.add(new_exam)
        db.session.commit()
        return redirect(url_for('add_question', exam_id=new_exam.id))
    
    return render_template('add_exam.html',exams=exams, form=form)

@app.route('/add_question/<int:exam_id>', methods=['GET', 'POST'])
@login_required
def add_question(exam_id):
    if current_user.role != 'admin':
        return redirect(url_for('home'))

    form = AddQuestionForm()
    if form.validate_on_submit():
        new_question = Question(question_text=form.question_text.data, exam_id=exam_id)
        db.session.add(new_question)
        db.session.commit()

        # Add choices
        choices = [
            form.choice_1.data,
            form.choice_2.data,
            form.choice_3.data,
            form.choice_4.data
        ]

        for i, choice_text in enumerate(choices):
            is_correct = (str(i + 1) == form.correct_choice.data)
            choice = Choice(choice_text=choice_text, is_correct=is_correct, question_id=new_question.id)
            db.session.add(choice)

        db.session.commit()
        flash('Question and choices added!', 'success')
        return redirect(url_for('add_question', exam_id=exam_id))

    return render_template('add_question.html', form=form)

@app.route('/exam_list', methods=['GET', 'POST'])
@login_required
def exam_list():
    if current_user.role == 'admin':
        return redirect(url_for('home'))
    exams = Exam.query.all()
    return render_template('exam_list.html', exams=exams)


@app.route('/exams/<int:exam_id>/<int:question_num>', methods=['GET', 'POST'])
@login_required
def take_exam_question(exam_id, question_num):
    if current_user.role == 'admin':
        return redirect(url_for('home'))
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()# Ensure the queston number is valid
    if question_num <= 0 or question_num > len(questions):
        return redirect(url_for('exam_list'))
    current_question = questions[question_num - 1]
    if request.method == 'POST':
        selected_choice = request.form.get('choice')
        if question_num < len(questions):
            return redirect(url_for('take_exam_question', exam_id=exam_id, question_num=question_num+ 1))
        else:
            return redirect(url_for('home', exam_id=exam_id))
    return render_template('take_exam_question.html', exam=exam, question=questions[question_num - 1],
                            question_num=question_num, total_questions=len(questions))
    #return redirect(url_for('login'))
