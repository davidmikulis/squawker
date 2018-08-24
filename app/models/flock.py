from app import db
from app.models.mutable_dict import MutableDict, JSONEncodedDict

class FlockModel(db.Model):
    __tablename__ = 'flocks'

    flock_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    name = db.Column(db.String(64))
    config = db.Column(MutableDict.as_mutable(JSONEncodedDict))

    def __init__(self, user_id, name, config):
        self.user_id = user_id
        self.name = name
        self.config = config

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
        return cls.query.filter_by(user_id = user_id).all()

    @classmethod
    def find_by_name(cls, user_id, name):
        return cls.query.filter_by(user_id = user_id, name = name).first()
