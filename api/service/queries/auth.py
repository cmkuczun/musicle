from .oracle import execute
import requests

def create_user(username, password):
    ''' create a new user given username/password
        returns: new user id (if success) or False (something went wrong)
    '''
    # create a new user
    q = "INSERT INTO usr (user_id, username, password) SELECT COALESCE(MAX(user_id), -1) + 1, '{}', '{}' FROM usr".format(username, password)
    execute(q)
    # check that you can login as the user (it exists/was created successfully)
    check_insert = login(username, password)
    if check_insert:
        # return user_id of new user
        return check_insert
    # return False
    print("ERROR: Something went wrong when creating account for {}.".format(username))
    return False
    
def login(username, password):
    ''' checks for matching username/password row in usr table
        returns: user_id if exists or None if does not exist
    '''
    # try to get the user id
    q = "select user_id from usr where username='{}' and password='{}'".format(username,password)
    res = execute(q)
    print(res)
    if len(res) > 0:
        # return user_id if exists
        user_id = res[0][0]
        return user_id
    # return NULL
    return None
