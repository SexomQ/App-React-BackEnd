# Import necessary modules
from flask import request, jsonify
import json
from models.database import db
from models.movies_saved import CineplexMovies, HappyMovies
from __main__ import app

@app.route('/api/cineplex-movies', methods=['GET'])
def get_cineplex_movies():
    # Get all Cineplex Movies from the database
    movies = CineplexMovies.query.all()
    # Serialize the data for the response
    if movies is not None:
        data = []
        for movie in movies:
            data.append({
                "id": movie.id_local,
                "title": movie.title,
                "category": movie.category,
                "img": movie.img,
                "url": movie.url
            })
        return jsonify(data), 200
    else:
        return jsonify({"error": "No movies found"}), 404
    
@app.route('/api/happy-movies', methods=['GET'])
def get_happy_movies():
    # Get all Happy Movies from the database
    movies = HappyMovies.query.all()
    # Serialize the data for the response
    if movies is not None:
        data = []
        for movie in movies:
            data.append({
                "id": movie.id_local,
                "title": movie.title,
                "category": movie.category,
                "img": movie.img,
                "url": movie.url
            })
        return jsonify(data), 200
    else:
        return jsonify({"error": "No movies found"}), 404
    
@app.route('/api/update_movies/cineplex', methods=['PUT'])
def update_cineplex_movies():
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
    
@app.route('/api/update_movies/happy', methods=['PUT'])
def update_happy_movies():
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
    
@app.route('/api/clear-cineplex', methods=['DELETE'])
def clear_cineplex_movies():
    try:
        # check password
        password = request.headers.get('X-Delete-Password')
        print(password)
        if password == "1234":  
            # Delete all Cineplex Movies
            CineplexMovies.query.delete()
            db.session.commit()
            return jsonify({"message": "Cineplex Movies deleted successfully"}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/clear-happy', methods=['DELETE'])
def clear_happy_movies():
    try:
        # check password
        password = request.headers.get('X-Delete-Password')
        if password == "1234":
            # Delete all Happy Movies
            HappyMovies.query.delete()
            db.session.commit()
            return jsonify({"message": "Happy Movies deleted successfully"}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500