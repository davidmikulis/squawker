from app import db
from app.models.flock import FlockModel

class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(64))
    access_token_secret = db.Column(db.String(64))
    last_flock_id = db.Column(db.Integer)
    flocks = db.relationship('FlockModel', backref='user')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def last_flock(self):
        return FlockModel.query.filter_by(flock_id=self.last_flock_id).first()

    def __init__(self, access_token, access_token_secret):
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def save_to_db(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def flock_names(self):
        return {
            "flock_names": [flock.name for flock in self.flocks]
        }

    def json_me(self):
        return {
            "user_id": self.user_id,
            "access_token": self.access_token,
            "last_flock_id": self.last_flock_id
        }

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id = user_id).first()

    @classmethod
    def find_by_access_token(cls, access_token):
        return cls.query.filter_by(access_token = access_token).first()

    @classmethod
    def find_by_id_and_token(cls, user_id, access_token):
        return cls.query.filter_by(user_id = user_id, access_token = access_token).first()