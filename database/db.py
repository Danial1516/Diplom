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

class TestQuestion(Base):
    __tablename__ = 'test_questions'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    level_id = Column(Integer, ForeignKey('level.id'))  # Связь с уровнем сложности
    level = relationship('Level')  # Связь с таблицей уровней

class TestAnswer(Base):
    __tablename__ = 'test_answers'
    id = Column(Integer, primary_key=True, index=True)
    first_option = Column(Text, nullable=False)
    second_option = Column(Text, nullable=False)
    third_option = Column(Text, nullable=False)
    is_correct = Column(Text, nullable=False)  # Признак правильного ответа
    question_id = Column(Integer, ForeignKey('test_questions.id'))  # Связь с вопросом
    question = relationship('TestQuestion')  # Обратная связь с вопросом


class TrueFalseQuestion(Base):
    __tablename__ = 'true_false_answer'
    id = Column(Integer, primary_key=True, index=True)
    correct_answer = Column(Boolean, nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship('Question')


class FillInQuestion(Base):
    __tablename__ = 'fill_in_answer'
    id = Column(Integer, primary_key=True, index=True)
    correct_answer = Column(String(255), nullable=False)
    first_choice = Column(Text, nullable=False)
    second_choice = Column(Text, nullable=False)
    third_choice = Column(Text, nullable=False)
    correct_answer = Column(String(255), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship('Question')


# Создание таблиц
def create_tables():
    Base.metadata.create_all(engine)
    logging.debug("Tables created successfully")
    seed_levels()
    seed_audio()
    seed_questions()
    seed_fill_in_answers()
    seed_true_false_answers()
    seed_test_questions()
    seed_test_answers()


def seed_true_false_answers():
    true_false_questions = [
        (1, True, 1),
        (2, False, 2),
        (3, True, 3),
        (4, True, 4),
        (5, False, 5),
        (6, True, 11),
        (7, False, 12),
        (8, False, 13),
        (9, True, 14),
        (10, True, 15)

    ]

    session = SessionLocal()

    for id, correct_answer, question_id in true_false_questions:
        try:
            true_false_question = TrueFalseQuestion(
                id=id,
                correct_answer=correct_answer,
                question_id=question_id
            )
            session.merge(true_false_question)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Failed to insert or update TrueFalseQuestion {id}: {e}")

    session.close()



def seed_fill_in_answers():
    fill_in_questions = [
        (1, "lifestyle", "diet", "lifestyle", "immune system", 6),
        (2, "blue", "blue", "yellow", "red", 7),
        (3, "circadian", "cardiac", "circadian", "circular", 8),
        (4, "quiet", "quiet", "noisy", "bright", 9),
        (5, "caffeine", "caffeine", "water", "sugar", 10),
        (6, "main menu", "dessert menu", "drink menu", "main menu", 16),
        (7, "pasta", "steak", "pasta", "salad", 17),
        (8, "peanuts", "dairy", "peanuts", "gluten", 18),
        (9, "glass of wine", "soda", "glass of wine", "water", 19),
        (10, "bill", "bill", "dessert menu", "manager", 20)
    ]

    session = SessionLocal()

    for id, correct_answer, first_choice, second_choice, third_choice, question_id in fill_in_questions:
        try:
            fill_in_question = FillInQuestion(
                id=id,
                correct_answer=correct_answer,
                first_choice=first_choice,
                second_choice=second_choice,
                third_choice=third_choice,
                question_id=question_id
            )
            session.merge(fill_in_question)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Failed to insert or update FillInQuestion {id}: {e}")

    session.close()

def seed_test_questions():
    questions = [
        # A1-A2 Level Questions
        (1, "She ___ to school every day.", 2),
        (2, "She is ___ the bus.", 2),
        (3, "They ___ happy today.", 2),
        (4, "I ___ reading a book right now.", 2),
        (5, "He ___ a car.", 2),
        (6, "We ___ to visit grandma tomorrow.", 2),
        (7, "He was born ___ 1995.", 2),
        (8, "They ___ football on weekends.", 2),
        (9, "She ___ like pizza.", 2),
        (10, "The cat is ___ the table.", 2),
        (11, "He always ___ TV in the evening.", 2),
        (12, "We will meet ___ Monday.", 2),

        # B2+ Level Questions
        (13, "She ___ to Paris three times.", 4),
        (14, "I ___ to play football when I was a child.", 4),
        (15, "You ___ finish your homework before going out.", 4),
        (16, "The party is ___ the weekend.", 4),
        (17, "She ___ start a new job next week.", 4),
        (18, "They ___ watching TV when I called.", 4),
        (19, "When I was young, I ___ play outside all day.", 4),
        (20, "She is interested ___ learning new languages.", 4),
        (21, "He ___ studying for three hours.", 4),
        (22, "The book is ___ the shelf.", 4),
        (23, "We ___ go to the beach every summer.", 4),
        (24, "She ___ to work late last night.", 4),
        (25, "By the time they move next month, they ___ made all necessary preparations.", 4),
        (26, "I ___ to have long hair.", 4),

        # C1+ Level Questions
        (27, "By the time we arrived, they ___", 5),
        (28, "He ___ always bring flowers on Sundays.", 5),
        (29, "You ___ wear a helmet when riding a bike.", 5),
        (30, "I knew they ___ be late.", 5),
        (31, "She lives ___ the outskirts of town.", 5),
        (32, "By next year, I ___ completed the course.", 5),
        (33, "We ___ eat dinner at 6 PM every day.", 5),
        (34, "Had I known the truth, I ___ you.", 5),
        (35, "The report is due ___ the end of the week.", 5),
    ]

    session = SessionLocal()

    for id, text, level_id in questions:
        try:
            question = TestQuestion(id=id, text=text, level_id=level_id)
            session.merge(question)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Failed to insert or update question {id}: {e}")

    session.close()


def seed_test_answers():
    answers = [
        # A1-A2 Level Answers
        (1, "go", "goes", "going", "goes", 1),
        (2, "at", "in", "on", "on", 2),
        (3, "is", "are", "am", "are", 3),
        (4, "is", "are", "am", "am", 4),
        (5, "has", "have", "having", "has", 5),
        (6, "going", "goes", "are going", "are going", 6),
        (7, "in", "at", "on", "in", 7),
        (8, "play", "plays", "playing", "play", 8),
        (9, "don’t", "doesn’t", "didn’t", "doesn’t", 9),
        (10, "under", "on", "above", "under", 10),
        (11, "watch", "watches", "watching", "watches", 11),
        (12, "in", "on", "at", "on", 12),

        # B2+ Level Answers
        (13, "has been", "was", "have been", "has been", 13),
        (14, "used", "use", "uses", "used", 14),
        (15, "has to", "have to", "had to", "have to", 15),
        (16, "at", "in", "on", "on", 16),
        (17, "will", "would", "is going to", "is going to", 17),
        (18, "was", "were", "are", "were", 18),
        (19, "would", "used", "will", "would", 19),
        (20, "at", "in", "on", "in", 20),
        (21, "has been", "is", "was", "has been", 21),
        (22, "in", "on", "at", "on", 22),
        (23, "would", "use to", "will", "used to", 23),
        (24, "had", "have", "has", "had", 24),
        (25, "have been", "are going to have", "will have", "will have", 25),
        (26, "used", "was used", "use", "used", 26),

        # C1+ Level Answers
        (27, "had left", "left", "was leaving", "had left", 27),
        (28, "would", "used", "was", "would", 28),
        (29, "must", "have to", "should", "must", 29),
        (30, "would", "will", "are going to", "would", 30),
        (31, "on", "in", "at", "on", 31),
        (32, "will have", "would have", "have", "will have", 32),
        (33, "used to", "would", "will", "would", 33),
        (34, "would have told", "tell", "will tell", "would have told", 34),
        (35, "by", "at", "in", "by", 35)
    ]
    session = SessionLocal()

    for id, first_option, second_option, third_option, is_correct, question_id in answers:
        try:
            fill_in_question = TestAnswer(
                id=id,
                first_option=first_option,
                second_option=second_option,
                third_option=third_option,
                is_correct=is_correct,
                question_id=question_id
            )
            session.merge(fill_in_question)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Failed to insert or update FillInQuestion {id}: {e}")

    session.close()

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


