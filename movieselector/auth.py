# auth.py
from sheets_service import read_all_records, append_record

def user_exists(username: str) -> bool:
    users = read_all_records()
    for user in users:
        if user.get("username") == username:
            return True
    return False

def register_user(username, password):
    if user_exists(username):
        return False
    # Append as a list, matching your sheet column order
    append_record([username, password])
    return True


def check_login(username: str, password: str) -> bool:
    users = read_all_records()
    for user in users:
        if user.get("username") == username and user.get("password") == password:
            return True
    return False
