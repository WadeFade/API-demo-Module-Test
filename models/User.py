from datetime import datetime
from dataclasses import dataclass
import bcrypt
import pytz
from conf import *
from sqlalchemy_utils import UUIDType


@dataclass
class User(db.Model):
    # id: UUIDType(binary=False)
    # alternative_id: UUIDType(binary=False)
    public_name: str
    first_name: str
    last_name: str
    email: str
    activated: bool
    admin: bool
    created_at: datetime
    last_login: datetime

    id = db.Column(UUIDType(binary=False), primary_key=True)
    alternative_id = db.Column(UUIDType(binary=False), unique=True, nullable=False)
    public_name = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), unique=False, nullable=False)
    activated = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    admin = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False,
                           default=datetime.now(pytz.timezone('Europe/Paris')))
    last_login = db.Column(db.DateTime, unique=False, nullable=True)

    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

    def verify_password(self, password):
        return bcrypt.checkpw(password, bytes.fromhex(self.password_hash[2:]))
