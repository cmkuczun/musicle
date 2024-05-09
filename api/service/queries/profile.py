from .oracle import execute
from datetime import datetime, timedelta

def get_user_streak(user_id):
    # First, get the daily puzzles which the current user has submitted a correct guess for
    q = f"""
    SELECT DISTINCT p.puzzle_date
    FROM guess g
    JOIN puzzle p ON g.puzzle_id = p.puzzle_id
    WHERE p.user_id IS NULL
      AND g.user_id = {user_id}
      AND g.is_correct = 1
    ORDER BY p.puzzle_date DESC
    """
    dates = execute(q)
    # print(dates)
    if dates is None or not dates or len(dates) is 0:
        return 0
    
    # If the user has any solved dailies, calculate current streak
    dates = [date[0] for date in dates]
    # print("datetype: ", type(dates[0]))
    streak = 0
    now = datetime.now()
    current_date = datetime(now.year,now.month,now.day, 0, 0, 0)
    # Go back day by day until we find a missing day, that's the streak
    for d in dates:
        # print("IN HERE:", d, current_date, d == current_date)
        if d == current_date:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    return streak

def get_user_best_streak(user_id):
    q = f"""
    SELECT DISTINCT p.puzzle_date
    FROM guess g
    JOIN puzzle p ON g.puzzle_id = p.puzzle_id
    WHERE p.user_id IS NULL
      AND g.user_id = {user_id}
      AND g.is_correct = 1
    ORDER BY p.puzzle_date DESC
    """
    dates = execute(q)

    if dates is None or not dates or len(dates) is 0:
        return 0
    elif len(dates) == 1:
        return 1

    dates = [date[0] for date in dates]

    best_streak = 1 # If they've played at least 1 daily puzzle, then best streak is at least 1
    current_streak = 1
    current_date = dates.pop(0)
    current_date -= timedelta(days=1)
     
    for date in dates:
        if date == current_date:
            current_streak += 1
            current_date -= timedelta(days=1)
        else:
            best_streak = max(best_streak, current_streak)
            current_streak = 1
            current_date = date 
            current_date - timedelta(days=1)
            
    # Check if the current streak extends beyond the loop
    best_streak = max(best_streak, current_streak)
    
    return best_streak


def user_total_solved(user_id):
    q = f'''
        select count(*)
        from guess
        where user_id = {user_id} and is_correct = 1
        '''
    res = execute(q)
    if not res:
        return 0
    else:
        return res[0][0]


def user_avg_guesses(user_id):
    q = f'''
        select avg(guess_num) 
        from guess
        where user_id = {user_id} and is_correct = 1
        '''

    res = execute(q)
    if not res:
        return 0
    else:
        return res[0][0]

def load_user_recent_games(user_id):
    q = f"""
    SELECT * FROM (
    SELECT p.puzzle_id,
       p.puzzle_date,
       MAX(g.guess_num) AS highest_guess_num,
       MAX(g.is_correct) AS solved_status
    FROM puzzle p
    LEFT JOIN guess g ON p.puzzle_id = g.puzzle_id
    WHERE g.user_id = {user_id}
    GROUP BY p.puzzle_id, p.puzzle_date
    ORDER BY p.puzzle_date DESC
    ) WHERE ROWNUM <= 10
    """

    puzzles = execute(q)
    if not puzzles:
        return []
    
    # Format the date strings
    puzzles = [list(puzzle) for puzzle in puzzles]
    for i, puzzle in enumerate(puzzles):
        puzzles[i][1] = puzzles[i][1].strftime('%m/%d/%Y')

    return puzzles
