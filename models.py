from app import db

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
