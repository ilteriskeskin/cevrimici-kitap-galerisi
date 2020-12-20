from flask import Flask, render_template, redirect, url_for, request, session, flash, json, jsonify
from forms import LoginForm, RegisterForm, SearchForm
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from database import db
from functools import wraps
from apis import Apis

app = Flask(__name__)

app.config['SECRET_KEY'] = "MemurBeySelcuk"

db.init()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Bu sayfayı görüntülemek için lütfen giriş yapın.', 'danger')
            return redirect(url_for('login'))

    return decorated_function


@app.route('/',  methods=['GET', 'POST'])
@login_required
def home():
    form = SearchForm()
    user = db.find_one('user', query={'email':session['email']})
    if request.method == "POST":
        searchVariable = form.search.data
        result = Apis.search_api(search_variable=searchVariable)
        books = result['books']
        return render_template('html/home.html', form=form, books=books, searchVariable=searchVariable, user=user)

    return render_template('html/home.html', form = form, user=user)

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
            'avatar': form.avatar.data,
            'favs':{}

            }

        db.insert_one('user', new_user)
        

        return redirect(url_for('login'))

    return render_template('html/register.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/profile', methods=["GET"])
@login_required
def profile():
    user = db.find_one("user", query={'email':session['email']})
    fav_books = []
    if user['favs']:
        fav_arrays = user['favs']['favs']
        for number in fav_arrays:
            last_number = number[27:]
            r = Apis.numeric_search(last_number)
            fav_books.append(r.json())   
    return render_template('html/profile.html', user=user, fav_books=fav_books)

@app.route('/fav/<url>', methods=['GET','POST'])
@login_required
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
