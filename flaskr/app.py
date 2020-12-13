from flask import Flask, render_template, redirect, url_for, request, session
from models import db 
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = "MemurBeySelcuk"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/tasn4/Desktop/github/cevrimici-kitap-galerisi/flaskr/secret.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
def __repr__(self):
    return '<User %r>' % self.username


with app.app_context():
    db.init_app(app)
    db.create_all()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    
    return render_template('login.html', form = form)

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    # Creating RegistrationForm class object
    form = RegisterForm()

    # Cheking that method is post and form is valid or not.
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        # if all is fine, generate hashed password
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        # create new user model object
        new_user = User(

            name = form.name.data, 

            email = form.email.data, 

            password = hashed_password,

            
            avatar = form.avatar.data) 

        # saving user object into data base with hashed password
        db.session.add(new_user)

        db.session.commit()

        # if registration successful, then redirecting to login Api
        return redirect(url_for('login'))

    else:

        # if method is Get, than render registration form
        return render_template('register.html', form = form)
@app.route('/logout/')
def logout():
    # Removing data from session by setting logged_flag to False.
    session['logged_in'] = False
    # redirecting to home page
    return redirect(url_for('home'))


    # Creating database tables



if __name__ == "__main__":
    app.run(debug=True)
