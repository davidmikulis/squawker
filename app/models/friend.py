from app import db

class FriendModel(db.Model):
    __tablename__ = 'friends'

    key = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    screen_name = db.Column(db.String(16))
    name = db.Column(db.String(64))
    verified = db.Column(db.Boolean)
    profile_image_url_https = db.Column(db.String(128))

    def __init__(self, user_id, screen_name, name, verified, profile_image_url_https):
        self.user_id = user_id
        self.screen_name = screen_name
        self.name = name
        self.verified = verified
        self.profile_image_url_https = profile_image_url_https

    def save_to_db(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def bulk_save_to_db(self, friend_list):
        db.session.bulk_save_objects(friend_list)
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id = user_id).first()

    @classmethod
    def find_by_user_id_list(cls, user_id_list):
        return cls.query.filter(cls.user_id.in_(user_id_list)).all()