from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_user
from nurse.user.forms import RegistrationForm, LoginForm
from nurse.user.models import User
from nurse import db

user_blueprint = Blueprint('user',
                           __name__,
                           template_folder='templates')


@user_blueprint.route('/registration', methods=['GET', 'POST'])
def new_user_registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("რეგისტრაცია წარმატებით დასრულდა")
        return redirect(url_for('user.login'))
    return render_template('registration.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash(f"მომხამრებელმა {user} წარმატებით გაიარა ავტორიზაცია")

            redirect_to = request.args.get('next')

            if redirect_to is None:
                redirect_to = url_for('homepage.representation')

            return redirect(redirect_to)

    return render_template('login.html', form=form)
