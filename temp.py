from flask import Flask, render_template, url_for, flash, redirect
import os
from flask_sqlalchemy import SQLAlchemy
from form import SignUpForm, LoginForm
app = Flask('__name__')

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:User(79542)@localhost/exams'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(25), nullable=False)
    lastName = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"User('{self.email}', '{self.firstName}')"

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            user = UserProfile.query.filter_by(email=form.email.data).first()
            if user and user.password == form.password.data:
                return redirect(url_for('home'))
            else:
                flash("wrong email or password", "success")
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = UserProfile(firstName=form.firstName.data,
                           lastName=form.lastName.data,
                           email=form.email.data,
                           password=form.password.data)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
