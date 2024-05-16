from app import create_app, db, CineplexMovies, HappyMovies

def init_database(db):
    app = create_app(db)
    with app.app_context():
        db.create_all()
        db.session.add(CineplexMovies(id_local=1, title='The Shawshank Redemption', category='Drama', img='https://www.imdb.com/title/tt0111161/mediaviewer/rm2488434432/', url='https://www.imdb.com/title/tt0111161/'))
        db.session.commit()

if __name__ == '__main__':
    init_database(db)
    