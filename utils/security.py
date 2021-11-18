import uuid
import jwt
from conf import app, db
from models.User import User


def verify_authentication(headers):
    if headers.get('Authorization'):
        token_unverified = headers.get('Authorization')[7:]
        if validation_jwt(token_unverified):
            id_not_tested = (jwt.decode(token_unverified, key=app.config['SECRET_KEY'], algorithms='HS256'))['id']
            test_user_connexion = User.query.filter_by(alternative_id=id_not_tested).first()
            if test_user_connexion:
                return test_user_connexion
    return None


def logout_user(headers):
    token = headers.get('Authorization')[7:]
    id_to_change = (jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256'))['id']
    user = User.query.filter_by(alternative_id=id_to_change).first()
    user.alternative_id = uuid.uuid4()
    db.session.update(user)
    db.session.commit()
    return True


def validation_jwt(token_unverified):
    try:
        jwt.decode(token_unverified, key=app.config['SECRET_KEY'], algorithms='HS256')
    except:
        return False
    return True
