from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_marshmallow import Marshmallow
import bcrypt
import json
from json import JSONEncoder
import jsonpickle
from flask.json import JSONEncoder

# init app
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
# print(dir(db.session))
db.init_app(app)
ma = Marshmallow(app)


# Models:
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(500))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    #
    # def __repr__(self):
    #     return f"Person('{self.username}', '{self.email}')"

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clothing_type = db.Column(db.String(100))
    occasion = db.Column(db.String(100))
    color = db.Column(db.String(100))
    season = db.Column(db.String(100))
    image = db.Column(db.String(500))

    def __init__(self, clothing_type, occasion, color, season, image):
        self.clothing_type = clothing_type
        self.occasion = occasion
        self.color = color
        self.season = season
        self.image = image
    #
    # def serialize(self):
    #     return {
    #         'gene_id': self.gene_id,
    #         'gene_symbol': self.gene_symbol,
    #         'p_value': self.p_value,
    #     }

    # def __repr__(self):
    #     return f"Item('{self.clothing_type}', '{self.occasion}', '{self.color}', '{self.season}', '{self.image}')"


# class PersonEncoder(JSONEncoder):
#     def default(self, o):
#         return o.__dict__
#
#
# class ItemEncoder(JSONEncoder):
#     def default(self, o):
#         return o.__dict__


# Schemas:
class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'clothing_type', 'occasion', 'color', 'season', 'image')


# Routes
# users = [{
#     "username": "Mills",
#     "email": "Mills@email.com",
#     "password": "Password"
# },
#     {
#         "username": "Jeff",
#         "email": "Jeff@email.com",
#         "password": "Password1"
#     },
#     {
#         "username": "Esters",
#         "email": "Ester@email.com",
#         "password": "Password2"
#     }]


@app.route('/api/v1/persons', methods=['GET'])
def get_persons():
    people = Person.query.all()
    data = persons_schema.dump(people)
    return jsonify(data), 200


@app.route('/api/v1/person', methods=['POST'])
def create_person():
    data = request.data
    json_formatted_data = json.loads(data)

    username = json_formatted_data['username']
    email = json_formatted_data['email']
    password = bcrypt.hashpw(json_formatted_data['password'].encode('utf8'), bcrypt.gensalt())

    new_user = Person(username, email, password)

    db.session.add(new_user)
    db.session.commit()
    # import pdb;
    # pdb.set_trace()

    return new_user.serialize(), 201


#
# @app.route('/api/v1.0/tasks/<int:id>', methods=['GET'])
# def get_task(id):
#     user = [user for user in users if user['id'] == id]
#     if len(user) == 0:
#         abort(404)
#     return jsonify({'task': user[0]})


# Init Schema:
person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)
item_schema = ItemSchema()

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

if __name__ == '__main__':
    app.run()
