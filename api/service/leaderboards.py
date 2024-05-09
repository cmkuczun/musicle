import pprint
from datetime import datetime, timedelta
from .queries.leaderboards import *

def curr_streak_rankings_service():
    rankings = get_top_10_by_streak()
    return rankings

def best_streak_rankings_service():
    rankings = get_top_10_by_overall_streak()
    return rankings

def num_solves_rankings_service():
    rankings = get_top_10_by_solves()
    return rankings

def avg_guess_rankings_service():
    rankings = get_top_10_by_avg_rounds()
    return rankings

def most_freq_song_service():
    song = most_freq_guessed_song()
    return song

def most_freq_artist_service():
    artist = most_freq_guessed_artist()
    return artist

def total_solved_count_service():
    count = get_overall_total_solved()
    return count

def avg_guess_count_service():
    count = get_avg_solved_game_len()
    return count
