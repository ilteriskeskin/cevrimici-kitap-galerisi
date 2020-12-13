from flask import Flask, render_template
from models import db 
from forms import LoginForm, RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "MemurBeySelcuk"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/tasn4/Desktop/github/cevrimici-kitap-galerisi/flaskr/secret.db'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/login', methods=['GET','POST'])
def login():
    loginForm = LoginForm()
    
    return render_template('login.html', loginForm = loginForm)


if __name__ == "__main__":
    app.run(debug=True)
