from flask import request, jsonify, Response
from models.User import *
from utils.security import *


# Endpoint to login : Params(email, password), Return: JWT
@app.route("/login/", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.verify_password(str.encode(data['password'])):
        token = jwt.encode(
            {'id': str(user.alternative_id), 'admin': user.admin,
             'exp': datetime.now(pytz.timezone('Europe/Paris')) + timedelta(hours=24)},
            app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({
            'token': token
        }), 200
    return jsonify({
        'error': 'Wrong email or password'
    }), 401


# Endpoint to logout the current user (using JWT)
@app.route("/logout/", methods=["POST"])
def logout():
    auth = verify_authentication(request.headers)
    if auth:
        user = User.query.filter_by(alternative_id=auth.alternative_id).first()
        user.alternative_id = uuid.uuid4()
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'user logged out successfully'
        }), 200
    return jsonify({
        'status': 'error',
        'message': 'Need to be logged in to logout'
    }), 403
