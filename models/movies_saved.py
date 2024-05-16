from models.database import db

class HappyMovies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_local = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(256), nullable=False)


    def __init__(self, id_local, title, category, img, url):
        self.id_local = id_local
        self.title = title
        self.category = category
        self.img = img
        self.url = url

class CineplexMovies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_local = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(256), nullable=False)


    def __init__(self, id_local, title, category, img, url):
        self.id_local = id_local
        self.title = title
        self.category = category
        self.img = img
        self.url = url