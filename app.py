from os import environ
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from olt.olt import Olt
from db import db
from models.users import User
from models.olt import Olt as OltModel

ISP = environ.get('ISP') or 'Provedor'
DB_URL = environ.get('DATABASE_URL') or 'sqlite:///db.sqlite3'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
auth = HTTPBasicAuth()


@app.before_first_request
def create_db():
    db.create_all()
    if not User.find_by_login('admin'):
        admin = User('admin', 'admin', True)
        admin.save_to_db()


@auth.verify_password
def verify_password(username, password):
    if username:
        user = User.find_by_login(username)
        if user and check_password_hash(user.password, password):
            return user


@app.route("/", methods=["GET", "POST"])
@auth.login_required
def index():
    olts = OltModel.find_all()
    print(
        f"Usuário {auth.current_user().username} logado.")
    return render_template("index.html", isp=ISP, olts=olts)


@app.route("/upgrade", methods=["POST"])
@auth.login_required
def upgrade():
    serial = request.form.get("serial")
    # TODO - Store request in database for audit purposes
    print(
        f"Usuário {auth.current_user().username} solicitou upgrade " +
        f"na ONT {serial}.")
    olt_id = request.form.get("olt")
    olt_data = OltModel.find_by_id(olt_id)
    olt = Olt(olt_data.olt_ip, olt_data.olt_port, olt_data.olt_usr,
              olt_data.get_password())
    port, onu_id = olt.get_onu_by_serial(serial)
    if port is None or onu_id is None:
        return render_template("notfound.html", serial=serial)
    olt.upgrade_onu(port, onu_id)
    return render_template("upgrade.html", serial=serial, port=port,
                           onu_id=onu_id)


@app.route("/admin", methods=["GET", "POST"])
@auth.login_required
def admin():
    olts = OltModel.find_all()
    if User.find_by_login(auth.current_user().username).is_admin:
        users = User.find_all()
        return render_template("admin.html", users=users, olts=olts)
    return "You are not admin!"


@app.route("/create_user", methods=["POST"])
@auth.login_required
def create_user():
    if User.find_by_login(auth.current_user().username).is_admin:
        username = str(request.form.get("user_username"))
        password = str(request.form.get("user_password"))
        is_admin = bool(request.form.get("is_admin"))
        user = User(username, password, is_admin)
        user.save_to_db()
        print(f"Usuário {auth.current_user().username}" +
              f"criou usuário {username}.")
        return "User created!"


@app.route("/create_olt", methods=["POST"])
@auth.login_required
def create_olt():
    if User.find_by_login(auth.current_user().username).is_admin:
        olt_name = str(request.form.get("olt_name"))
        olt_ip = str(request.form.get("olt_ip"))
        olt_port = str(request.form.get("olt_port"))
        olt_usr = str(request.form.get("olt_usr"))
        olt_pwd = str(request.form.get("olt_pwd"))
        olt = OltModel(olt_name, olt_ip, olt_port, olt_usr, olt_pwd)
        olt.save_olt_to_db()
        print(f"Usuário {auth.current_user().username}" +
              f"criou OLT {olt_name}.")
        return "OLT created!"


@app.route("/delete_user", methods=["POST"])
@auth.login_required
def delete_user():
    if User.find_by_login(auth.current_user().username).is_admin:
        username = str(request.form.get("user_username"))
        user = User.find_by_login(username)
        if user:
            user.delete_user()
            print(f"Usuário {auth.current_user().username}" +
                  f"deletou usuário {username}.")
            return "User deleted!"
        return "User not found!"
    return "You are not admin!"


@app.route("/delete_olt", methods=["POST"])
@auth.login_required
def delete_olt():
    if User.find_by_login(auth.current_user().username).is_admin:
        olt_id = str(request.form.get("olt_id"))
        olt = OltModel.find_by_id(olt_id)
        if olt:
            olt.delete_olt()
            print(f"Usuário {auth.current_user().username}" +
                  f"deletou OLT {olt_id}.")
            return "OLT deleted!"
        return "OLT not found!"
    return "You are not admin!"


if __name__ == "__main__":
    app.run()
