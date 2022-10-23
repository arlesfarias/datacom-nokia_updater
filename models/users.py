from db import db
from werkzeug.security import generate_password_hash


class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(102), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, is_admin=False) -> None:
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    @classmethod
    def find_by_login(self, username) -> 'User':
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        return None

    @classmethod
    def find_all_admins(self) -> list:
        return User.query.filter_by(is_admin=True).all()

    @classmethod
    def find_all(self) -> list:
        return User.query.all()

    def save_to_db(self) -> None:
        self.password = generate_password_hash(self.password)
        db.session.add(self)
        db.session.commit()

    def delete_user(self) -> None:
        db.session.delete(self)
        db.session.commit()
