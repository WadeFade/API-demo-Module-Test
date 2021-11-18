import re
from flask import request, Response, jsonify
from models.User import *
from utils.security import *


@app.route("/user/", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def user():
    # GET : to get every User stored in BDD
    if request.method == 'GET':
        auth = verify_authentication(request.headers)
        if auth:
            users = User.query.all()
            return jsonify(users), 200
        return jsonify({
            'status': 'Unauthorized',
            'message': 'Invalid token'
        }), 401
    # POST : to register a new User (email is unique)
    elif request.method == 'POST':
        data = request.get_json()
        if re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", data['email']):
            check_user = User.query.filter_by(email=data['email']).first()
            if check_user is None:
                password = str.encode(data['password'])
                new_user = User(id=uuid.uuid4(), alternative_id=uuid.uuid4(), public_name=data['public_name'],
                                first_name=data['first_name'].capitalize(),
                                last_name=data['last_name'].upper(),
                                email=data['email'], password=password,
                                created_at=datetime.now(pytz.timezone('Europe/Paris')))
                db.session.add(new_user)
                db.session.commit()
                return Response(status=201)
        return jsonify({
            'status': 'Bad request',
            'message': 'Invalid email or email already used'
        }), 400
    # PATCH : to patch user who is currently logged (using JWT)
    elif request.method == 'PATCH':
        auth = verify_authentication(request.headers)
        if auth:
            data = request.get_json()
            user = User.query.filter_by(alternative_id=auth.alternative_id).first()
            user.public_name = data['public_name']
            user.last_name = data['last_name'].upper()
            user.first_name = data['first_name'].capitalize()
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'User patched successfully'
            }), 200
        else:
            return jsonify({
                'status': 'Unauthorized',
                'message': 'Invalid token'
            }), 401
    #     DELETE : to delete User who is currently logged (using JWT)
    elif request.method == 'DELETE':
        auth = verify_authentication(request.headers)
        if auth:
            user_to_delete = User.query.filter_by(alternative_id=auth.alternative_id).first()
            if user_to_delete:
                db.session.delete(user_to_delete)
                db.session.commit()
                return jsonify({
                    'status': 'success',
                    'message': 'User deleted successfully'
                }), 200
            return jsonify({
                'status': 'Bad request'
            }), 400
        else:
            return jsonify({
                'status': 'Unauthorized',
                'message': 'Invalid token'
            }), 401
