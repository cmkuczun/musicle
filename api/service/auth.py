from .queries.auth import *

def login_service(username, password):
    user_id = login(username, password)
    return user_id

def register_service(username, password):
    user_id = create_user(username, password)
    return user_id
