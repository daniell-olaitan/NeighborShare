#!/usr/bin/python3
"""
Module implements all authentication views
"""
from flask import render_template, flash, jsonify
from flask import redirect, url_for, request
from flask_login import current_user, login_required
from flask_login import logout_user
from . import auth
from models import db
import uuid
from app.forms.authforms import SignInForm, ResetPasswordForm
from app.forms.authforms import PasswordResetForm, SignUpForm
from models.user import User
from app import simple_geoip


@auth.route('/register', methods=['GET', 'POST'],
            strict_slashes=False)
def register():
    cache_id = str(uuid.uuid4())
    form = SignUpForm()
    if form.validate_on_submit():
        print(simple_geoip.get_geoip_data())
        geoip_data = simple_geoip.get_geoip_data()['location']
        latitude = geoip_data['lat']
        longitude = geoip_data['lng']
        print(latitude, longitude)
        user = User(email=form.email.data,
                    password=form.password.data,
                    username=form.username.data,
                    home_address=form.address.data,
                    latitude=latitude, longitude=longitude
        )
        token = user.generate_confirmation_token()
        user.send_account_confirmation_link(token)
        db.save(user)
        user.signin_user(False)
        flash('You can now sign in.')
        return redirect(url_for('auth.login'))

    print(form.errors)      #debug
    return render_template('auth/signup.html', form=form,
                           cache_id=cache_id)


@auth.route('/login', methods=['GET', 'POST'],
            strict_slashes=False)
def login():
    cache_id = str(uuid.uuid4())
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.authenticate_user(
            form.password.data):
            user.signin_user(form.keep_session.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.home')
            return redirect(next)
        flash('Invalid Username of Password')
    return render_template('auth/signin.html', form=form,
                           cache_id=cache_id)


@auth.route('/confirm/<token>', strict_slashes=False)
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('auth.login'))
    if current_user.confirm_token(token):
        db.session.commit()
        flash('You have confirmed your account.')
        return redirect(url_for('auth.login'))
    else:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('main.index'))


@auth.route('/logout', strict_slashes=False)
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/password-reset', methods=['GET', 'POST'],
            strict_slashes=False)
def password_reset():
    cache_id = str(uuid.uuid4())
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            token = user.generate_password_token()
            user.send_password_reset_link(token)
            user.signin_user(False)
            flash('A reset link has been sent to your email')
            return redirect(url_for('auth.login'))
        flash('Invalid Email')
    return render_template('auth/password_reset.html', form=form,
                           cache_id=cache_id)


@auth.route('/password-reset/<token>', strict_slashes=False)
def confirm_password_reset(token):
    if current_user.confirm_password_token(token):
        return redirect(url_for('auth.reset_password'))
    else:
        flash('The reset link is invalid or has expired.')
        return redirect(url_for('auth.login'))


@auth.route('/reset-password', methods=['GET', 'POST'],
            strict_slashes=False)
def reset_password():
    cache_id = str(uuid.uuid4())
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.save(current_user)
        flash('You have reset your password')

        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form,
                           cache_id=cache_id)


@auth.before_app_request
def before_request():
    if (current_user.is_authenticated and
        not current_user.confirmed and
        request.blueprint != 'auth'
            and request.endpoint != 'static'):
        return render_template('auth/unconfirmed.html')
