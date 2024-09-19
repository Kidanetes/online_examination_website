"""this module will define routes to be used by the user"""


from flask import render_template, url_for, flash, redirect, request
from online_examination import app, db, bcrypt
from online_examination.form import SignUpForm, LoginForm, UpdatePassword
from online_examination.models import UserProfile
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
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
                           password=hashed_password)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash("account created sucessfully", "success")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    """logout the logged in user"""
    logout_user()
    return redirect(url_for('home'))

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
