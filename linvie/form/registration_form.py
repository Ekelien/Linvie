from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class PasswordValid(object):
    def __init__(self):
        self.message = "Your password must contain at least 8 characters, with at least one letter and one digit."

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().letters() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Your username is required'),
        Length(min=3, message='Your username is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')
