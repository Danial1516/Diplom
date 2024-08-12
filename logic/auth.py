# logic/auth.py

from database.db import db
import logging
import datetime
logging.basicConfig(level=logging.DEBUG)

def login_user(email, password):
    user = db.login_user(email, password)
    return user is not None

def register_user(name, email, password):
    result = db.register_user(name, email, password)
    if result:
        logging.debug(f"User {email} registered successfully.")
    else:
        logging.error(f"Failed to register user {email}. User might already exist.")
    return result

def user_login(self, email, password):
    user = self.login_user(email, password)
    if user:
        user_id = user[0]
        login_date = datetime.now().date()
        self.record_login(user_id, login_date)
        streak = self.get_login_streak(user_id)
        logging.debug(f"User {email} has a login streak of {streak} days")
        return True
    return False
