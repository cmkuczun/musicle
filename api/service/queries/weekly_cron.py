import sys
import os
import logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from queries.inserts import insert_puzzle
from queries.oracle import execute
from datetime import timedelta,datetime
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler

# logger to check if cron job has been created
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# get a daily song!
def get_random_song_id():
    '''returns: random song id that has not yet been used for a puzzle''' 
    q="""	
		SELECT *
		FROM (
    		SELECT s.song_id
    		FROM song s
    		LEFT JOIN puzzle p ON s.song_id = p.song_id
    		AND p.song_id IS NULL
    		ORDER BY DBMS_RANDOM.VALUE
		) WHERE ROWNUM = 1
	""" 
    res = execute(q)
    if not (res and len(res)):
        return None
    return res[0][0]

# create the daily puzzles for this week
def add_weekly_songs():
    # generate next week's dates
    current_datetime = datetime.now()
    week_dates = [current_datetime + timedelta(days=i) for i in range(7)]
    formatted_dates = [date.strftime("%Y-%m-%d") for date in week_dates]
    user_id=None
    for d in formatted_dates:
        # get random song id
        song_id = get_random_song_id()
        # create a new puzzle for that day
        insert_puzzle(song_id,user_id,d)
        sleep(.5)


sched = BackgroundScheduler()
sched.add_job(add_weekly_songs, 'cron', day_of_week='0', hour='12')
sched.start()

# if __name__=='__main__':
    # add_weekly_songs()
