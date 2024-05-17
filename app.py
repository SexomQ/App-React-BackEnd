from flask import Flask
import os
import dotenv
from datetime import timedelta

from models.movies_saved import CineplexMovies, HappyMovies
from models.database import db
from flask_swagger_ui import get_swaggerui_blueprint

dotenv.load_dotenv()

def create_app(db):
    SWAGGER_URL="/swagger"
    API_URL="/static/swagger.json"


    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Access API'
        }
    )

    app = Flask(__name__)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies_saved.db'

    # JWT
    app.config["JWT_SECRET_KEY"] = "test_key"  # test
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)

    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app(db)
    import routes
    app.run(debug=True)