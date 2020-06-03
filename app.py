from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_marshmallow import Marshmallow
import bcrypt
import json

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

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username
        }


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    clothing_type = db.Column(db.String(100))
    occasion = db.Column(db.String(100))
    color = db.Column(db.String(100))
    season = db.Column(db.String(100))
    image = db.Column(db.String(500))

    def __init__(self, description, clothing_type, occasion, color, season, image):
        self.description = description
        self.clothing_type = clothing_type
        self.occasion = occasion
        self.color = color
        self.season = season
        self.image = image

    def serialize(self):
        return {
            'description': self.description,
            'clothing_type': self.clothing_type,
            'occasion': self.occasion,
            'color': self.color,
            'season': self.season,
            'image': self.image,
        }


# Schemas:
class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description', 'clothing_type', 'occasion', 'color', 'season', 'image')


# Routes
# Return all Users
@app.route('/api/v1/persons', methods=['GET'])
def get_persons():
    people = Person.query.all()
    data = persons_schema.dump(people)
    return jsonify(data), 200


# Create User
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

    return new_user.serialize(), 201


# Return singular user
@app.route('/api/v1/person/<id>', methods=['GET'])
def get_person(id):
    person = Person.query.get(id)
    data = person_schema.dump(person)

    return jsonify(data), 200


# Delete User
@app.route('/api/v1/person/<id>', methods=['DELETE'])
def delete_person(id):
    person = Person.query.get(id)
    db.session.delete(person)
    db.session.commit()

    people = Person.query.all()
    data = persons_schema.dump(people)

    return jsonify(data), 204


# Create Item
@app.route('/api/v1/item', methods=['POST'])
def create_item():
    data = request.data
    json_formatted_data = json.loads(data)

    description = json_formatted_data['description']
    clothing_type = json_formatted_data['clothing_type']
    occasion = json_formatted_data['occasion']
    color = json_formatted_data['color']
    season = json_formatted_data['season']
    image = json_formatted_data['image']

    new_item = Item(description, clothing_type, occasion, color, season, image)

    db.session.add(new_item)
    db.session.commit()

    return item_schema.jsonify(new_item), 201


@app.route('/api/v1/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    data = items_schema.dump(items)
    return jsonify(data), 200


# Init Schema:
person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

if __name__ == '__main__':
    app.run()
