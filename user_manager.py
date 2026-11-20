from myandradb_link import load_user, load_learning, save_message, update_session_summary, get_context
from myandradb_link import create_user_record

def find_user_profile(user_id):
    return load_user(user_id)

def user_exists(user_id):
    profile = find_user_profile(user_id)

    if profile:
        return True

    return False

def create_guest_user():
    return None

def create_user(name):
    return create_user_record(name)
