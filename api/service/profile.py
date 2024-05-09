from datetime import datetime, timedelta
from .queries.profile import *

def curr_streak_service(user_id):
    streak = get_user_streak(user_id)
    return streak

def best_streak_service(user_id):
    streak = get_user_best_streak(user_id)
    return streak

def total_solved_service(user_id):
    count = user_total_solved(user_id)
    return count

def avg_guesses_service(user_id):
    count = user_avg_guesses(user_id)
    return count

def recent_games_service(user_id):
    recent = load_user_recent_games(user_id)
    return recent
