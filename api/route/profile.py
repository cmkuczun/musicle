from http import HTTPStatus
from flask import Blueprint, request, jsonify
import sys
sys.path.append("..")
from service.profile import *

profile_api = Blueprint('profile', __name__)

@profile_api.route('/<user_id>/curr_streak/', methods=['GET'])
def curr_streak(user_id):
    streak = curr_streak_service(user_id)
    return jsonify(streak), HTTPStatus.OK

@profile_api.route('/<user_id>/best_streak/', methods=['GET'])
def best_streak(user_id):
    streak = best_streak_service(user_id)
    return jsonify(streak), HTTPStatus.OK

@profile_api.route('/<user_id>/total_solved/', methods=['GET'])
def total_solved(user_id):
    solved = total_solved_service(user_id)
    return jsonify(solved), HTTPStatus.OK

@profile_api.route('/<user_id>/avg_guesses/', methods=['GET'])
def avg_guesses(user_id):
    avg = avg_guesses_service(user_id)
    return jsonify(avg), HTTPStatus.OK

@profile_api.route('/<user_id>/recent_games/', methods=['GET'])
def recent_games(user_id):
    games = recent_games_service(user_id)
    return jsonify(games), HTTPStatus.OK
