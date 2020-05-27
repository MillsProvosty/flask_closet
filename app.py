from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

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
db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


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


# db.create_all()
guest = User(email='guest@example.com', password='password', username='Mills')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

if __name__ == '__main__':
    app.run()
