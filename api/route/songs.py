from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import sys
sys.path.append("..")
from service.songs import get_guess_list_service
import logging
import pprint

songs_api = Blueprint('songs', __name__)

@songs_api.route('/<song_id>/', methods=['GET'])
@cross_origin()
def get_song(song_id):
    '''get song by song_id'''
    return jsonify(get_song_service(song_id)), HTTPStatus.OK

@songs_api.route('/similarlist/', methods=['POST'])
@cross_origin()
def get_guess_list():
    '''get list of songs that fit guessed criteria'''
    data = request.json
    formatted_json = pprint.pformat(data)
    # print(formatted_json)
    # print(get_guess_list_service(data))
    return jsonify(get_guess_list_service(data)), HTTPStatus.OK

    
@songs_api.route('/<puzzle_id>/<user_id>/<song_id>/', methods=['POST'])
@cross_origin()
def put_guess(puzzle_id, user_id, song_id):
    '''put a guess in the database'''
    return jsonify(put_guess(puzzle_id, user_id, song_id)), HTTPStatus.OK

