from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

from nurse.user.models import User


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('pass_confirm')])
    pass_confirm = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("register")

    def validate_user_from_db(self, username):
        temp_username = self.username.data
        if User.find_by_username(temp_username):
            raise ValidationError("User already exists")


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Login")
