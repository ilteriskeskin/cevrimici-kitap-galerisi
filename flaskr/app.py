from flask import Flask, render_template, redirect, url_for, request, session, flash, json, jsonify
from models import db, User
from forms import LoginForm, RegisterForm, SearchForm
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "MemurBeySelcuk"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secret.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/',  methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if request.method == "POST":
        searchVariable = form.search.data
        searchUrl = 'https://api.itbook.store/1.0/search/'
        
        r = requests.get(searchUrl + searchVariable) 
        result = r.json()
        books = result['books']
        return render_template('index.html', form=form, books = books)

    return render_template('index.html', form = form)
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    # Creating Login form object
    form = LoginForm()
    # verifying that method is post and form is valid
    if request.method == 'POST' and form.validate:
        # checking that user is exist or not by email
        user = User.query.filter_by(email = form.email.data).first()

        if user:
            # if user exist in database than we will compare our database hased password and password come from login form 
            if check_password_hash(user.password, form.password.data):
                # if password is matched, allow user to access and save email and username inside the session
                flash('You have successfully logged in.', "success")

                session['logged_in'] = True

                session['email'] = user.email 

            
                # After successful login, redirecting to home page
                return redirect(url_for('home'))

            else:

                # if password is in correct , redirect to login page
                flash('Username or Password Incorrect', "Danger")

                return redirect(url_for('login'))
    # rendering login page
    return render_template('login.html', form = form)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        new_user = User(
            name = form.name.data,
            email = form.email.data,
            password = hashed_password,
            avatar = form.avatar.data)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


# entry point
if __name__ == "__main__":
    app.run(debug=True)
