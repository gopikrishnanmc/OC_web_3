from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_mail import Mail


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = True
app.config['USER_APP_NAME'] = 'OpenClinical.net'
app.config['USER_AFTER_REGISTER_ENDPOINT'] = 'user.login'
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())


db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/profile')
@login_required
def profile():
    return '<h1>This is the protected profile page</h1>'


if __name__ == '__main__':
    app.run(debug=True)
