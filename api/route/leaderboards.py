from http import HTTPStatus
from flask import Blueprint, request, jsonify
import sys
sys.path.append("..")
from service.leaderboards import *

leaderboards_api = Blueprint('leaderboards', __name__)

@leaderboards_api.route('/currStreakRankings/', methods=['GET'])
def get_curr_streak_rankings():
    rankings = curr_streak_rankings_service()
    return jsonify(rankings), HTTPStatus.OK

@leaderboards_api.route('/bestStreakRankings/', methods=['GET'])
def get_best_streak_rankings():
    rankings = best_streak_rankings_service()
    return jsonify(rankings), HTTPStatus.OK

@leaderboards_api.route('/numSolvesRankings/', methods=['GET'])
def get_num_solves_rankings():
    rankings = num_solves_rankings_service()
    return jsonify(rankings), HTTPStatus.OK

@leaderboards_api.route('/avgGuessRankings/', methods=['GET'])
def get_avg_guess_rankings():
    rankings = avg_guess_rankings_service()
    return jsonify(rankings), HTTPStatus.OK

@leaderboards_api.route('/mostFreqSong/', methods=['GET'])
def get_most_freq_song():
    song = most_freq_song_service()
    return jsonify(song), HTTPStatus.OK

@leaderboards_api.route('/mostFreqArtist/', methods=['GET'])
def get_most_freq_artist():
    artist = most_freq_artist_service()
    return jsonify(artist), HTTPStatus.OK

@leaderboards_api.route('/totalSolvedCount/', methods=['GET'])
def get_total_solved_count():
    count = total_solved_count_service()
    return jsonify({"count": count}), HTTPStatus.OK

@leaderboards_api.route('/avgGuessCount/', methods=['GET'])
def get_avg_guess_count():
    count = avg_guess_count_service()
    return jsonify({"count": count}), HTTPStatus.OK
