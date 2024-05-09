from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import sys
sys.path.append("..")
from service.users import *
from flasgger import swag_from

users_api = Blueprint('users', __name__)

@users_api.route('/', methods=['GET'])
@swag_from('user_specs.yml')
def get_users():
    '''get all users'''
    users = get_all_users_service()
    return jsonify({'users': users}), HTTPStatus.OK

@users_api.route('/<int:user_id>/', methods=['GET'])
@swag_from('./docs/get_user.yml')
def get_user(user_id):
    '''get user by user_id'''
    return jsonify(get_user_service(user_id)), HTTPStatus.OK

# I can break this down depending on how it's used in the frontend
@users_api.route('/<user_id>/stats/', methods=['GET'])
def get_user_stats(user_id):
    '''get user and global stats'''
    user_stats = get_user_stats_service(user_id)
    global_stats = get_global_stats_service(user_id)

    if not (user_stats):
        return jsonify(
            {"user_stats": None,
            "global_stats" : None}
            ), HTTPStatus.INTERNAL_SERVER_ERROR

    return jsonify(
        {"user_stats": user_stats,
        "global_stats" : global_stats}
        ), HTTPStatus.OK

@users_api.route('<user_id>/streak_stats/', methods=['GET'])
def get_user_streak_stats(user_id):
    '''get current streak and best streak for user id'''
    user_streak_stats = get_user_stats_service(user_id)

    if not (user_streak_stats):
        return jsonify({"best_streaak":0, "current_streak":0}), HTTPStatus.INTERNAL_SERVER_ERROR

    return jsonify(user_streak_stats), HTTPStatus.OK

# @users_api.route('/stats/', methods=['GET'])
# def get_global_stats():
#     '''get global stats'''
#     return jsonify(get_global_stats_service()), HTTPStatus.OK

@users_api.route('/<user_id>/<puzzle_id>/', methods=['GET'])
@cross_origin()
def get_past_guesses(user_id, puzzle_id):
    '''get past guesses for user'''
    past_guesses = get_past_guesses_service(user_id, puzzle_id)
    if past_guesses:
        return jsonify(past_guesses), HTTPStatus.OK
    else:
        return jsonify({"message": "No Guesses Found"}), HTTPStatus.INTERNAL_SERVER_ERROR

@users_api.route('/puzzle/create/', methods=['POST'])
@cross_origin()
def create_user_puzzle2():
    data = request.json
    if not data:
        return jsonify({'error': 'No Config Provided'}), HTTPStatus.BAD_REQUEST
    puzzle_id, config = create_user_puzzle_service(data["minYear"], data["maxYear"], data["genres"], data["user_id"])
    if config == None:
        return jsonify({'error': 'No songs matched the params'}), HTTPStatus.BAD_REQUEST
    return jsonify({"puzzle_id" : puzzle_id, "config": config}), HTTPStatus.OK

@users_api.route('/puzzle/<date>/', methods=['GET'])
@cross_origin()
def get_daily_puzzle(date):
    '''retrieve puzzle from date'''
    puzzle_id, config = get_puzzle_from_date_service(date)
    print("puzzle", puzzle_id, config)
    if puzzle_id and config:
        return jsonify({"puzzle_id" : puzzle_id, "config": config}), HTTPStatus.OK
    return jsonify({"message": "No puzzle for that date"}), HTTPStatus.INTERNAL_SERVER_ERROR

@users_api.route('/puzzle/config/<puzzle_id>/', methods=['GET'])
@cross_origin()
def get_puzzle_from_id(puzzle_id):
    '''retrieve puzzle from date'''
    config = get_config_from_puzzle_id_service(puzzle_id)
    if config:
        return jsonify({"config": config}), HTTPStatus.OK
    return jsonify({"message": "No puzzle for that ID"}), HTTPStatus.INTERNAL_SERVER_ERROR


# @users_api.route('/puzzle/<user_id>/', methods=["POST"])
# @cross_origin()
# def create_user_puzzle(user_id):
#     data = request.json
#     if not data:
#         return jsonify({'error': 'No Config Provided'}), HTTPStatus.BAD_REQUEST
#     puzzle_id, config = create_user_puzzle_service(data["startdate"], data["enddate"], data["genres"], user_id)
#     if config == None:
#         return jsonify({'error': 'No songs matched the params'}), HTTPStatus.BAD_REQUEST
#     return jsonify({"puzzle_id" : puzzle_id, "config": config}), HTTPStatus.OK



    

### CHECK GUESS FUNCTION
@users_api.route('/<user_id>/<puzzle_id>/<song_id>/<guess_num>/', methods=["POST"])
@cross_origin()
def check_guess(user_id, puzzle_id, song_id, guess_num):
    data = request.json
    if not data:
        return jsonify({'error': 'No Config Provided'}), HTTPStatus.BAD_REQUEST
    correct = check_correct_service(song_id, puzzle_id)
    if insert_guess_service(user_id, puzzle_id, song_id, guess_num, correct):
        print("success on insert new guess")
        updated_config = get_config_from_puzzle_id_service(puzzle_id)
        if not correct:
            updated_config = diff_configs_service(data, updated_config, song_id)
        else:
            updated_config = set_known_to_true_utility(updated_config)
        return jsonify({"updated_config": updated_config, "correct": correct}), HTTPStatus.OK
    return {}, HTTPStatus.INTERNAL_SERVER_ERROR

@users_api.route('/config/<song_id>/', methods=["GET"])
def get_config_from_song_id(song_id):
    return jsonify(get_blank_config_from_song_id_service(song_id)), HTTPStatus.OK


@users_api.route('/<user_id>/get_recent_puzzles/', methods=["GET"])
def get_user_recent_puzzles(user_id):
    puzzles = get_recent_puzzles_service(user_id)
    return jsonify(puzzles), HTTPStatus.OK
