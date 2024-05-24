# Import necessary modules
from flask import request, jsonify
from flask_cors import CORS
import json

from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from models.database import db
from models.movies_saved import CineplexMovies, HappyMovies
from __main__ import app

# JWT
jwt = JWTManager(app)

# Enable CORS
CORS(app)

@app.route('/api/login/<string:user_type>', methods=['POST'])
def login(user_type):
    access_token = create_access_token(identity=user_type)
    return jsonify(access_token=access_token), 200

@app.route('/api/movies/<string:cinema>', methods=['GET'])
@jwt_required()
def manipulate_movies(cinema):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 4, type=int)
    
    if cinema == 'cineplex':
        # Get paginated Cineplex Movies from the database
        movies_query = CineplexMovies.query
        movies_pagination = movies_query.paginate(page=page, per_page=per_page, error_out=False)
        movies = movies_pagination.items

        # Serialize the data for the response
        if movies:
            data = [
                {
                    "id": movie.id_local,
                    "title": movie.title,
                    "category": movie.category,
                    "img": movie.img,
                    "url": movie.url
                } for movie in movies
            ]
            response = {
                "movies": data,
                "total": movies_pagination.total,
                "pages": movies_pagination.pages,
                "current_page": page
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "No movies found"}), 404
    elif cinema == 'happy':
        # Get paginated Happy Movies from the database
        movies_query = HappyMovies.query
        movies_pagination = movies_query.paginate(page, per_page, error_out=False)
        movies = movies_pagination.items

        # Serialize the data for the response
        if movies:
            data = [
                {
                    "id": movie.id_local,
                    "title": movie.title,
                    "category": movie.category,
                    "img": movie.img,
                    "url": movie.url
                } for movie in movies
            ]
            response = {
                "movies": data,
                "total": movies_pagination.total,
                "pages": movies_pagination.pages,
                "current_page": page
            }
            return jsonify(response), 200
        else:
            return jsonify({"error": "No movies found"}), 404
            

@app.route('/api/movies/<string:cinema>', methods=['PUT'])
@jwt_required()
def update_movies(cinema):
    if cinema == 'cineplex':
        try:
            # Get data from the CineplexData.json file
            with open('static/CineplexData.json', 'r') as file:
                data = json.load(file)
            # Delete all existing Cineplex Movies
            CineplexMovies.query.delete()
            # Create new Cineplex Movies
            for movie in data:
                cineplex_movie = CineplexMovies(
                    id_local=movie['id'],
                    title=movie['title'],
                    category=movie['category'],
                    img=movie['img'],
                    url=movie['url']
                )
                db.session.add(cineplex_movie)
            db.session.commit()
            return jsonify({"message": "Cineplex Movies updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif cinema == 'happy':
        try:
            # Get data from the HappyData.json file
            with open('static/HappyData.json', 'r') as file:
                data = json.load(file)
            # Delete all existing Happy Movies
            HappyMovies.query.delete()
            # Create new Happy Movies
            for movie in data:
                happy_movie = HappyMovies(
                    id_local=movie['id'],
                    title=movie['title'],
                    category=movie['category'],
                    img=movie['img'],
                    url=movie['url']
                )
                db.session.add(happy_movie)
            db.session.commit()
            return jsonify({"message": "Happy Movies updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/api/movies/<string:cinema>', methods=['DELETE'])
@jwt_required()
def delete_movies(cinema):   
    if cinema == 'cineplex':
        try:
            # check password
            password = request.headers.get('X-Delete-Password')
            if password == "1234" and get_jwt_identity() == 'admin':
                # Delete all Cineplex Movies
                CineplexMovies.query.delete()
                db.session.commit()
                return jsonify({"message": "Cineplex Movies deleted successfully"}), 200
            else:
                return jsonify({"error": "Invalid password or you are anothorized"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif cinema == 'happy':
        try:
            # check password
            password = request.headers.get('X-Delete-Password')
            if password == "1234" and get_jwt_identity() == 'admin':
                # Delete all Happy Movies
                HappyMovies.query.delete()
                db.session.commit()
                return jsonify({"message": "Happy Movies deleted successfully"}), 200
            else:
                return jsonify({"error": "Invalid password or you are anothorized"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500
