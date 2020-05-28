from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_marshmallow import Marshmallow
import bcrypt
import json


# init app
# from sqlalchemy.testing.suite.test_reflection import users

app = Flask(__name__)

# config DB
POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'flask_closet',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
ma = Marshmallow(app)


# Models:
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))

    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    occasion = db.Column(db.String(100))
    color = db.Column(db.String(100))
    season = db.Column(db.String(100))
    image = db.Column(db.String(500))

    def __init__(self, type, occasion, color, season, image):
        self.type = type
        self.occasion = occasion
        self.color = color
        self.season = season
        self.image = image


# Schemas:
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'type', 'occasion', 'color', 'season', 'image')


# Routes
users = [{
    "id": 1,
    "username": "Mills",
    "email": "Mills@email.com",
    "password": "Password"
},
    {
        "id": 2,
        "username": "Jeff",
        "email": "Jeff@email.com",
        "password": "Password1"
    },
    {
        "id": 3,
        "username": "Esters",
        "email": "Ester@email.com",
        "password": "Password2"
    }]


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})


@app.route('/api/v1.0/tasks/<int:id>', methods=['GET'])
def get_task(id):
    user = [user for user in users if user['id'] == id]
    if len(user) == 0:
        abort(404)
    return jsonify({'task': user[0]})

# Init Schema:
user_schema = UserSchema()

item_schema = ItemSchema()


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

if __name__ == '__main__':
    app.run()
