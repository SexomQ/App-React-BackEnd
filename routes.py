# Import necessary modules
from flask import request, jsonify
import json
from models.database import db
from models.movies_saved import CineplexMovies, HappyMovies
from __main__ import app

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello, World!'