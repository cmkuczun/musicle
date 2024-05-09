from .oracle import execute
from .profile import *


# 1. Get the top 10 players ordered by current streak
def get_top_10_by_streak():
    ''' get top 10 players by daily streaks
        include the inputted user_id in top 10 or as an additional output
        returns: list of lists formatted as [user_id, streak, rank]
    '''
    # First, we want a list of all users who have solved a daily puzzle
    q = """
    SELECT u.user_id, u.username
    FROM usr u
    JOIN (
        SELECT DISTINCT g.user_id
        FROM guess g
        JOIN puzzle p ON g.puzzle_id = p.puzzle_id
        WHERE g.is_correct = 1
        AND p.user_id IS NULL
    ) completed_users ON u.user_id = completed_users.user_id
    """

    users = execute(q)
    if not users:
        return []
    users = list([list(user) for user in users])

    # Now, get the curr streak of each
    for i, user in enumerate(users):
        best_streak = get_user_streak(user[0])
        users[i].append(best_streak)

    # Sort the users by their curr streaks
    users = sorted(users, key=lambda x: x[2], reverse=True)

    # Filter to the 10 best users
    users = users[:10]
    
    # Finally, add their rank to their entry
    for i, user in enumerate(users):
        users[i] = [i+1, users[i][0], users[i][1], users[i][2]]

    return users

# 2. Get the top 10 players ordered by best streak of all time
def get_top_10_by_overall_streak(): 
    # First, we want a list of all users who have solved a daily puzzle
    q = """
    SELECT u.user_id, u.username
    FROM usr u
    JOIN (
        SELECT DISTINCT g.user_id
        FROM guess g
        JOIN puzzle p ON g.puzzle_id = p.puzzle_id
        WHERE g.is_correct = 1
        AND p.user_id IS NULL
    ) completed_users ON u.user_id = completed_users.user_id
    """

    users = execute(q)
    if not users:
        return []
    users = list([list(user) for user in users])

    # Now, get the best streak of each
    for i, user in enumerate(users):
        best_streak = get_user_best_streak(user[0])
        users[i].append(best_streak)

    # Sort the users by their best streaks
    users = sorted(users, key=lambda x: x[2], reverse=True)

    # Filter to the 10 best users
    users = users[:10]
    
    # Finally, add their rank to their entry
    for i, user in enumerate(users):
        users[i] = [i+1, users[i][0], users[i][1], users[i][2]]

    return users


# 3. Get the top 10 players ordered by total number of games solved
def get_top_10_by_solves():
    '''
    input: user id logged in
    gets the top 10 players who have solved the most puzzles, ordered by num of games solved
    returns: array of 10 or 11 usernames, and their guess count, and their place (ROWNUM) -> [place,username,guess_count]
        NOTE - include the inputted user id and their results whether they are in top 10 or not
    '''
    q = f'''
            WITH top_solvers AS (
    SELECT
        usr.user_id,
        usr.username,
        COUNT(DISTINCT puzzle.puzzle_id) AS num_solved_puzzles
    FROM
        guess
    INNER JOIN
        puzzle ON guess.puzzle_id = puzzle.puzzle_id
    INNER JOIN
        usr ON guess.user_id = usr.user_id
    WHERE
        guess.is_correct = 1
    GROUP BY
        usr.user_id, usr.username
    ORDER BY
        num_solved_puzzles DESC
    )
    SELECT
    ROWNUM AS rank,
    user_id,
    username,
    num_solved_puzzles
    FROM
    top_solvers
    WHERE
    ROWNUM <= 10
        '''
    res = execute(q)
    if res is None or len(res) == 0:
        return []
    return res
 
# 4. Get the top 10 players by average rounds needed to solve puzzles
def get_top_10_by_avg_rounds():
    ''' get top 10 players by lowest average rounds needed to solve puzzles 
        (including inputted user)
        returns: dictionary of {player id: average rounds}
    '''
    q = f"""
        WITH avg_guesses AS (
    SELECT
        guess.user_id,
        usr.username,
        AVG(CASE WHEN guess.is_correct = 1 THEN guess.guess_num END) AS avg_rounds
    FROM
        guess
    INNER JOIN
        usr ON guess.user_id = usr.user_id
    GROUP BY
        guess.user_id, usr.username
    ORDER BY
        avg_rounds ASC
    )
    SELECT
    ROWNUM AS rank,
    user_id,
    username,
    avg_rounds
    FROM
    avg_guesses
    WHERE
    ROWNUM <= 10
    """
    res = execute(q)
    if res == None or len(res) == 0:
        return []
    return list(res)

# 5. Total number of puzzle solves
def get_overall_total_solved():
    q = "SELECT COUNT(*) FROM guess WHERE is_correct = 1"
    res = execute(q)
    return (res[0][0] if res is not None else None)

# 6. Overall average guesse solve any puzzle by all players
def get_avg_solved_game_len():
    q = "SELECT AVG(guess_num) AS avg_guesses_to_solve FROM guess WHERE is_correct = 1"
    res = execute(q)
    return (res[0][0] if res is not None and len(res) > 0 else None)

# 7. Most frequently guessed song by all users over all guess
def most_freq_guessed_song():
    q = """
        SELECT s.song_name, a.artist_name, g.guess_count
        FROM (
            SELECT * 
            FROM (
                SELECT song_id, COUNT(*) AS guess_count
                FROM guess
                GROUP BY song_id
                ORDER BY guess_count DESC
            ) g
            WHERE ROWNUM = 1
        ) g
        JOIN song s ON g.song_id = s.song_id
        JOIN song_artist sa ON s.song_id = sa.song_id
        JOIN artist a ON sa.artist_id = a.artist_id
        WHERE ROWNUM = 1
    """

    res = execute(q) 
    return None if not (res and len(res)) else res[0]

# 8. Most frequently guessed artist by all users over all guesses
def most_freq_guessed_artist():
    q = """
        SELECT a.artist_name, g.guess_count
        FROM (
            SELECT *
            FROM (
                SELECT sa.artist_id, COUNT(*) AS guess_count
                FROM guess g
                JOIN song_artist sa ON g.song_id = sa.song_id
                GROUP BY sa.artist_id
                ORDER BY guess_count DESC
            ) g
            WHERE ROWNUM = 1
        ) g
        JOIN artist a ON g.artist_id = a.artist_id
        """

    res = execute(q)
    return None if not (res and len(res)) else res[0]
