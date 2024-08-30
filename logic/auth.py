from database.db import Database  # Импорт класса Database
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

# Создание экземпляра класса Database
db = Database()

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

def user_login(email, password):
    user = db.login_user(email, password)
    if user:
        user_id = user.id  # Изменение на user.id для SQLAlchemy
        login_date = datetime.now().date()
        result = db.record_login(user_id, login_date)
        if result:
            streak = db.get_login_streak(user_id)
            logging.debug(f"User {email} has a login streak of {streak} days")
            return True
    return False
