from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_marshmallow import Marshmallow

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



# Schemas:
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'type', 'occasion', 'color', 'season', 'image')


# Init Schema:
user_schema = UserSchema()

item_schema = ItemSchema()

# Routes:

# @app.route('/')
# def hello_world():
#     return 'Hello World!'


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

if __name__ == '__main__':
    app.run()
