#!/usr/bin/python3
"""
Module implements all authentication views
"""
from flask import jsonify, redirect, request, current_app
from itsdangerous import TimedSerializer as Serializer
from . import auth
from models import db
from app import jwt
from models.invalid_tokens import InvalidToken
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import get_jwt, create_refresh_token
from models.user import User


@auth.route('/register', methods=['POST'])
def register():
    form = request.get_json()

    try:
        user = User.query.filter_by(email=form['email']).first()
        if user:
            if user.confirmed:
                return jsonify({'error': 'Email has been chosen by another user.'})

            token = user.generate_confirmation_token()
            user.send_account_confirmation_link(token)
            return jsonify({'success': True})

        user = User.query.filter_by(username=form['username']).first()
        if user:
            return jsonify({'error': 'Username has been taken.'})

        user = User(email=form['email'], password=form['password'], username=form['username'])

        token = user.generate_confirmation_token()
        user.send_account_confirmation_link(token)
        db.save(user)
        return jsonify({'success': True})

    except:
        return jsonify({'error': 'Invalid Form'})


@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return InvalidToken.is_valid(jti)


@auth.route('/check-login-status', methods=['POST'])
@jwt_required()
def check_if_logged_in():
    return jsonify({'success': True})


@auth.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    access_token = create_access_token(identity=get_jwt_identity())
    return jsonify({'token': access_token})


@auth.route('/get-current-user')
@jwt_required()
def get_current_user():
    uid = get_jwt_identity()
    user = User.query.filter_by(id=uid).first()
    if user:
        return jsonify({'user': {'username': user.username, 'image': None}})

    return jsonify({'error': True})


@auth.route('/login', methods=['POST'])
def login():
    form = request.get_json()
    try:
        user = User.query.filter_by(email=form['email']).first()
        if user and user.authenticate_user(
                form['password']):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                return jsonify({'accessToken': access_token, 'refreshToken': refresh_token})
        else:
            return jsonify({'error': 'Wrong username or password'})
    except:
        return jsonify({'error': 'Invalid Form'})


@auth.route('/confirm/<token>')
def confirm_registration(token):
    s = Serializer(current_app.config['SECRET_KEY'], 'confirmation')
    message = 'success'

    try:
        email = s.loads(token, max_age=600).get('confirm')
        print(email)
    except:
        message = 'error'
        return redirect("{}/confirm-account/{}".format(current_app.config['FRONTEND_BASE_URL'], message))
    user = User.query.filter_by(email=email).first()
    if user:
        user.confirmed = True
        db.save(user)

    else:
        message = 'error'

    return redirect("{}/confirm-account/{}".format(current_app.config['FRONTEND_BASE_URL'], message))


@auth.route('/logout', strict_slashes=False)
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    user_token = InvalidToken(jti=jti)
    db.save(user_token)

    return {'success': True}


@auth.route('/reset-password', methods=['POST'])
def password_reset():
    form = request.get_json()
    user = User.query.filter_by(email=form['email']).first()
    if user:
        token = user.generate_password_token()
        user.send_password_reset_link(token)
        return jsonify({'success': True})

    return jsonify({'error': 'Invalid email'})


@auth.route('/confirm-password-reset/<token>')
def confirm_password_reset(token):
    s = Serializer(current_app.config['SECRET_KEY'], 'password')
    message = 'success'

    try:
        user_id = s.loads(token, max_age=600).get('password')
    except:
        message = 'error'
        return redirect("{}/password-confirmation/{}".format(current_app.config['FRONTEND_BASE_URL'], message))
    user = User.query.get(user_id)
    if user:
        user.password_reset_confirmed = True
        db.save(user)
        return redirect("{}/password-confirmation/{}".format(current_app.config['FRONTEND_BASE_URL'], message))

    else:
        message = 'error'

    return redirect("{}/password-confirmation/{}".format(current_app.config['FRONTEND_BASE_URL'], message))


@auth.route('/password-reset', methods=['POST'])
def reset_password():
    form = request.get_json()
    email = form['email']
    user = User.query.filter_by(email=email).first()
    if user and user.password_reset_confirmed:
        user.set_password(form['password'])
        user.password_reset_confirmed = False
        db.save(user)

        return jsonify({'success': True})

    return jsonify({'error': 'Invalid Email Address'})
