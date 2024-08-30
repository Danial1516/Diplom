from sqlalchemy import create_engine, Column, Integer, String, Date, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

# Настройка подключения к базе данных
DATABASE_URL = "postgresql+psycopg2://qwe:qwe@localhost:5432/langvoyage"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Определение моделей
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    progress = Column(Integer, default=0)


class UserLogin(Base):
    __tablename__ = 'user_logins'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    login_date = Column(Date, nullable=False)
    user = relationship('User', back_populates='logins')


User.logins = relationship('UserLogin', back_populates='user', cascade="all, delete-orphan")


class Level(Base):
    __tablename__ = 'level'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)


class Audio(Base):
    __tablename__ = 'audio'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship('Level')


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)
    audio_id = Column(Integer, ForeignKey('audio.id'))
    audio = relationship('Audio')


class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship('Question')


# Создание таблиц
def create_tables():
    Base.metadata.create_all(engine)
    logging.debug("Tables created successfully")
    seed_levels()
    seed_audio()
    seed_questions()



def seed_questions():
    questions = [
        (1, "Drinking a warm glass of milk before bed can help you fall asleep.", "tf", 1),
        (2, "Exercising right before bed is recommended for better sleep.", "tf", 1),
        (3, "Keeping a regular sleep schedule helps improve sleep quality.", "tf", 1),
        (4, "Using electronic devices before bed can disrupt your sleep.", "tf", 1),
        (5, "It's good to eat a heavy meal just before going to bed.", "tf", 1),
        (6, "A good night's sleep is important for maintaining a healthy _______.", "fill_in", 1),
        (7, "To avoid sleep problems, it's advised to reduce your exposure to _______ light before bedtime.", "fill_in", 1),
        (8, "The body's internal clock, known as the _______ rhythm, helps regulate sleep patterns.", "fill_in", 1),
        (9, "Keeping your bedroom cool, dark, and _______ can improve sleep quality.", "fill_in", 1),
        (10, "To get a better night's sleep, avoid consuming _______ late in the day.", "fill_in", 1),
        (11, "The customer asks for a vegetarian option.", "tf", 2),
        (12, "The waiter offers a discount on the meal.", "tf", 2),
        (13, "The customer orders dessert at the beginning of the meal.", "tf", 2),
        (14, "The customer is allergic to peanuts and asks about them in the dish.", "tf", 2),
        (15, "The waiter suggests trying the house special.", "tf", 2),
        (16, "The customer starts by asking to see the _______.", "fill_in", 2),
        (17, "The waiter recommends the _______ as a popular dish among customers.", "fill_in", 2),
        (18, "The customer asks if the dish contains _______ due to an allergy.", "fill_in", 2),
        (19, "The customer orders a _______ to drink with their meal.", "fill_in", 2),
        (20, "At the end of the meal, the customer asks for the _______.", "fill_in", 2),

    ]

    session = SessionLocal()

    for id, text, type, audio_id in questions:
        try:
            question = Question(id=id, text=text, type=type, audio_id=audio_id)
            session.merge(question)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Failed to insert or update question {id}: {e}")

    session.close()


# Функция для вставки или обновления данных в таблице Audio
def seed_audio():
    audios = [
        (1, "Ordering food", "https://drive.google.com/file/d/1oL3moK4d813HoQZNBGK0VqCc9FITyciX/view?usp=drive_link", 1),
        (2, "A good nights sleep", "https://drive.google.com/file/d/18HbCiGDuGT0bjhMLhfiy7h-1XoLvBcmL/view?usp=drive_link", 1),
        (4, "Free time", "https://drive.google.com/file/d/1OahEaH4GHnAH-JMt7nuhd_1OnYT-TwTt/view?usp=drive_link", 2),
        (5, "Stop wasting time", "https://drive.google.com/file/d/1px6D75-LxZkQIvdbBLL1m3EnY0HQ8P1H/view?usp=drive_link", 2),
        (6, "Advice for exams", "https://drive.google.com/file/d/1NuOnngm2ow_ReFBQQz1DbG4Yvmkg4e7j/view?usp=drive_link", 3),
        (7, "llamas", "https://drive.google.com/file/d/1b4VMTw5ee_g5jO4E-XOj5pAHWz4TmdnH/view?usp=drive_link", 3),
        (8, "How to study", "https://drive.google.com/file/d/1AgKYKl0v6lEVqMtEpKckKQJf8BxII1Lc/view?usp=drive_link", 4),
        (9, "Sports interviews", "https://drive.google.com/file/d/16azEO4Z8X7u5qR6veOXyHMOPpa5j1P8E/view?usp=drive_link", 4)
    ]

    session = SessionLocal()

    for id, name, url, level_id in audios:
        try:
            audio = Audio(id=id, name=name, url=url, level_id=level_id)
            session.merge(audio)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Failed to insert or update audio {id}: {e}")

    session.close()

def seed_levels():
    levels = [
        (1, "A1"),
        (2, "A2"),
        (3, "B1"),
        (4, "B2"),
        (5, "C1")
    ]

    session = SessionLocal()
    for id, name in levels:
        # Использование merge для обновления существующих записей и добавления новых
        level = Level(id=id, name=name)
        try:
            session.merge(level)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            logging.error(f"Failed to insert or update level {id}: {e}")

    session.close()


# Функции для работы с базой данных
class Database:
    def __init__(self):
        self.session = SessionLocal()

    def register_user(self, name, email, password):
        try:
            new_user = User(name=name, email=email, password=password)
            self.session.add(new_user)
            self.session.commit()
            logging.debug(f"User {email} registered successfully")
            return True
        except IntegrityError as e:
            self.session.rollback()
            logging.error(f"Failed to register user {email}: {e}")
            return False

    def login_user(self, email, password):
        user = self.session.query(User).filter_by(email=email, password=password).first()
        return user

    def record_login(self, user_id, login_date):
        try:
            new_login = UserLogin(user_id=user_id, login_date=login_date)
            self.session.add(new_login)
            self.session.commit()
            logging.debug(f"Login for user {user_id} recorded successfully")
            return True
        except IntegrityError as e:
            self.session.rollback()
            logging.error(f"Failed to record login for user {user_id}: {e}")
            return False

    def get_login_streak(self, user_id):
        logins = self.session.query(UserLogin).filter_by(user_id=user_id).order_by(UserLogin.login_date.desc()).all()
        dates = [login.login_date for login in logins]

        streak = 0
        if dates:
            current_date = datetime.now().date()
            for date in dates:
                if (current_date - date).days == streak:
                    streak += 1
                else:
                    break

        return streak


