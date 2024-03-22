#!/usr/bin/python3
"""
Module defines the login screen
"""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms import BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Regexp
from wtforms.validators import Length
from models.user import User


class SignInForm(FlaskForm):
    """
    Class implements the fields of the sign in form
    """
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    keep_session = BooleanField('keep me signed in?')
    submit = SubmitField('sign in')


class SignUpForm(FlaskForm):
    """
    class implements the fields of the sign up form
    """
    username = StringField('username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    email = StringField('email', validators=[DataRequired(), Email()])
    address = StringField('address', validators=[DataRequired()])
    password = PasswordField('password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.'),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])'
               '[A-Za-z\d@$!%*?&]{8,16}$', 0,
               'Password must be minimum of  and maximum 16 characters, at least '
               'one uppercase letter, one lowercase letter, one number '
               'and one special character')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('sign up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PasswordResetForm(FlaskForm):
    """
    Class implements a field for password reset form
    """
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('reset password')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is not registered.')


class ResetPasswordForm(FlaskForm):
    """
    Class implements a field for password reset form
    """
    password = PasswordField('password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.'),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])'
               '[A-Za-z\d@$!%*?&]{8,16}$', 0,
               'Password must be minimum of  and maximum 16 characters, at least '
               'one uppercase letter, one lowercase letter, one number '
               'and one special character')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('reset password')
