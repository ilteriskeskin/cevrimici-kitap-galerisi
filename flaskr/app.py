from flask import Flask, render_template, redirect, url_for, request, session, flash, json, jsonify
from models import db, User
from forms import LoginForm, RegisterForm, SearchForm
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from database import db

app = Flask(__name__)

app.config['SECRET_KEY'] = "MemurBeySelcuk"

db.init()


@app.route('/',  methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if request.method == "POST":
        searchVariable = form.search.data
        searchUrl = 'https://api.itbook.store/1.0/search/'
        
        r = requests.get(searchUrl + searchVariable) 
        result = r.json()
        books = result['books']
        return render_template('index.html', form=form, books=books)

    return render_template('index.html', form = form)
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    # Creating Login form object
    form = LoginForm()
    # verifying that method is post and form is valid
    if request.method == 'POST' and form.validate:
        # checking that user is exist or not by email
        user = db.find_one('user', query={'email':form.email.data})
        

        if user:
            # if user exist in database than we will compare our database hased password and password come from login form 
            if check_password_hash(user['password'], form.password.data):
                # if password is matched, allow user to access and save email and username inside the session
                flash('You have successfully logged in.', "success")

                session['logged_in'] = True

                session['email'] = user['email']

            
                # After successful login, redirecting to home page
                return redirect(url_for('home'))

            else:

                # if password is in correct , redirect to login page
                flash('Username or Password Incorrect', "Danger")

                return redirect(url_for('login'))
    # rendering login page
    return render_template('html/login.html', form = form)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate and request.method == 'POST':
        user = db.find_one('user', query={'email':form.email.data})
        if user:
            return redirect(url_for('login'))
        
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        new_user = {
 
            'name': form.name.data,
            'email': form.email.data,
            'password': hashed_password,
            'avatar': form.avatar.data

            }

        db.insert_one('user', new_user)
        

        return redirect(url_for('login'))

    return render_template('html/register.html', form=form)


@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route('/profile', methods=["GET"])
def profile():
    user = db.find_one("user", query={'email':session['email']})
    book_api_url = "https://api.itbook.store/1.0/books/"
    fav_arrays = user['favs']['favs']
    fav_books = []
    for number in fav_arrays:
        last_number = number[27:]
        r = requests.get(book_api_url + last_number)
        fav_books.append(r.json())
        
    return render_template('html/profile.html', user=user, fav_books=fav_books)

@app.route('/fav/<url>', methods=['GET','POST'])
def favourite(url):
    full_url = 'https://itbook.store/books/'+url
    user = db.find_one("user", query={'email':session['email']})
    if user['favs']:
        books = user['favs']
        books['favs'].append(full_url)
    else:
        books = {
            'favs': [full_url],
        }

    db.find_and_modify('user', 
                        query={'email':session['email']}, 
                        favs=books)
    return redirect(url_for('home'))
    


# entry point
if __name__ == "__main__":
    app.run(debug=True)
