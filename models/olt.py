from db import db
from utils.crypto_tools import encrypt, decrypt, generate_salt
from os import environ


SECRET = environ.get('SECRET') or 'supersecretpassword'


class Olt(db.Model):

    __tablename__ = 'olt'

    olt_id = db.Column(db.Integer, primary_key=True)
    olt_name = db.Column(db.String(32), unique=True, nullable=False)
    olt_ip = db.Column(db.String(32), unique=False, nullable=False)
    olt_port = db.Column(db.Integer, nullable=False)
    olt_usr = db.Column(db.String(32), nullable=False)
    olt_pwd = db.Column(db.String(160), nullable=False)
    salt = db.Column(db.String(64), nullable=False)

    def __init__(self, olt_name, olt_ip, olt_port, olt_usr, olt_pwd) -> None:
        self.olt_name = olt_name
        self.olt_ip = olt_ip
        self.olt_port = olt_port
        self.olt_usr = olt_usr
        self.olt_pwd = olt_pwd
        self.salt = generate_salt()

    def __repr__(self) -> str:
        return f"<Olt {self.olt_ip}>"

    @classmethod
    def find_by_id(self, olt_id) -> 'Olt':
        olt = Olt.query.filter_by(olt_id=olt_id).first()
        if olt:
            return olt
        return None

    def save_olt_to_db(self) -> None:
        self.olt_pwd = encrypt(self.olt_pwd, SECRET, self.salt)
        db.session.add(self)
        db.session.commit()

    def get_password(self) -> str:
        return decrypt(self.olt_pwd, SECRET, self.salt)

    @classmethod
    def find_all(self) -> list:
        return Olt.query.all()

    def delete_olt(self) -> None:
        db.session.delete(self)
        db.session.commit()
