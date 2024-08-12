# database/db.py

import psycopg2
import logging
import datetime
logging.basicConfig(level=logging.DEBUG)

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                dbname="langvoyage",
                user="qwe",
                password="qwe",
                host="localhost",
                port="5432"
            )
            self.cursor = self.connection.cursor()
            logging.debug("Database connection established")
        except psycopg2.OperationalError as e:
            logging.error("Failed to connect to the database")
            logging.error(e)
            raise

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            progress INTEGER DEFAULT 0
        )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_logins (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                login_date DATE NOT NULL,
                UNIQUE (user_id, login_date)
            )
            """)
        self.connection.commit()

    def register_user(self, name, email, password):
        try:
            self.cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            self.connection.commit()
            logging.debug(f"User {email} registered successfully")
            return True
        except psycopg2.IntegrityError as e:
            self.connection.rollback()
            logging.error(f"Failed to register user {email}: {e}")
            return False

    def login_user(self, email, password):
        self.cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        return self.cursor.fetchone()

    def record_login(self, user_id, login_date):
        try:
            self.cursor.execute("INSERT INTO user_logins (user_id, login_date) VALUES (%s, %s)", (user_id, login_date))
            self.connection.commit()
            logging.debug(f"Login for user {user_id} recorded successfully")
            return True
        except psycopg2.IntegrityError as e:
            self.connection.rollback()
            logging.error(f"Failed to record login for user {user_id}: {e}")
            return False

    def get_login_streak(self, user_id):
        self.cursor.execute("""
        SELECT login_date FROM user_logins
        WHERE user_id = %s
        ORDER BY login_date DESC
        """, (user_id,))
        dates = [row[0] for row in self.cursor.fetchall()]

        streak = 0
        if dates:
            current_date = datetime.now().date()
            for date in dates:
                if (current_date - date).days == streak:
                    streak += 1
                else:
                    break

        return streak


db = Database()
db.create_table()
