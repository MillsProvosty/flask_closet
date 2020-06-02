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


# Schemas:
class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'clothing_type', 'occasion', 'color', 'season', 'image')


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

    return new_user.serialize(), 201


@app.route('/api/v1/person/<id>', methods=['GET'])
def get_person(id):
    person = Person.query.get(id)
    data = person_schema.dump(person)

    return jsonify(data), 200

@app.route('/api/v1/person/<id>', methods=['DELETE'])
def delete_person(id):
    person = Person.query.get(id)
    db.session.delete(person)
    db.session.commit()

    people = Person.query.all()
    data = persons_schema.dump(people)

    return jsonify(data), 204



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
