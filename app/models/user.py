from app import db

class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(64))
    access_token_secret = db.Column(db.String(64))
    last_flock = db.Column(db.Integer, db.ForeignKey('flocks.flock_id'))

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

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id = user_id).first()

    @classmethod
    def find_by_access_token(cls, access_token):
        return cls.query.filter_by(access_token = access_token).first()

    @classmethod
    def find_by_id_and_token(cls, user_id, access_token):
        return cls.query.filter_by(user_id = user_id, access_token = access_token).first()