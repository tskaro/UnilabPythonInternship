from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Chapter10_User.projects.Giorgi_Tskaroveli.nurse.forms import RegistrationForm, LoginForm
from Chapter10_User.projects.Giorgi_Tskaroveli.nurse.models import User
import os

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
app = Flask(__name__)


def create_app():
    app.config['SECRET_KEY'] = "mySECRETkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CSRF_ENABLED'] = True
    app.config['USER_ENABLE_EMAIL'] = False

    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'login'

    @app.route('/', methods=['GET'])
    def homepage():
        return render_template('home.html')

    @app.route('/welcome', methods=['GET'])
    def welcome():
        return render_template('welcome.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.find_by_username(form.username.data)
            if user is not None and user.check_password(form.password.data):
                login_user(user)
                flash(f"მომხამრებელმა {user} წარმატებით გაიარა ავტორიზაცია")

                redirect_to = request.args.get('next')

                if redirect_to is None:
                    redirect_to = url_for('welcome')

                return redirect(redirect_to)

        return render_template('login.html', form=form)

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        logout_user()
        flash("მომხმარებელი გამოვიდა სისტემიდან")
        return redirect(url_for('homepage'))

    @app.route('/registration', methods=['GET', 'POST'])
    def new_user_registration():
        form = RegistrationForm

        if form.validate_on_submit():
            user = User(username=form.email.data,
                        password=form.email.data)

            db.session.add(user)
            db.session.commit()

            flash("რეგისტრაცია წარმატებით დასრულდა")
            return redirect(url_for('login'))
        return render_template('registration.html')

    return app


class NursesModel(db.Model):
    __tablename__ = "nurses"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    address = db.Column(db.String)
    department = db.Column(db.String)
    shift = db.Column(db.Integer)

    def __init__(self, email, first_name, last_name, address, department, shift):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.department = department
        self.shift = shift

    def __repr__(self):
        return f'Nurse email:{self.email}, name {self.first_name} {self.last_name}, address: {self.address},' \
               f'department: {self.department}, shift: {self.shift}'


from nurse.nurse_registration.views import nurse_blueprint

app.register_blueprint(nurse_blueprint, url_prefix="/")

from nurse.homepage.views import homepage

app.register_blueprint(homepage, url_prefix="/")



