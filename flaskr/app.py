from flask import Flask, render_template, redirect, url_for, request, session
from models import db, User
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = "MemurBeySelcuk"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secret.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return render_template('home.html')

    return render_template('login.html', form=form)

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
