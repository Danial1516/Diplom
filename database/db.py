from sqlalchemy import create_engine, Column, Integer, String, Date, Text, Boolean, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime
import random
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import func


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
    ratings = relationship("Rating", back_populates="user")


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Внешний ключ для связи с таблицей User

    # Поля для хранения времени в секундах и минутах, изменены на Numeric
    thirty_sec = Column(Numeric(precision=20, scale=2), default=0)  # Рейтинг для 30 секунд
    one_min = Column(Numeric(precision=20, scale=2), default=0)  # Рейтинг для 1 минуты
    three_min = Column(Numeric(precision=20, scale=2), default=0)  # Рейтинг для 3 минут

    # Определение отношения с таблицей User
    user = relationship("User", back_populates="ratings")

class UserLogin(Base):
    __tablename__ = 'user_logins'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    login_date = Column(Date, nullable=False)
    user = relationship('User', back_populates='logins')


User.logins = relationship('UserLogin', back_populates='user', cascade="all, delete-orphan")


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)

class Level(Base):
    __tablename__ = 'level'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    sentences = relationship("Sentence", back_populates="level")

class Sentence(Base):
    __tablename__ = 'sentences'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    level_id = Column(Integer, ForeignKey('level.id'), nullable=False)

    level = relationship("Level", back_populates="sentences")
    words = relationship("SentenceWord", back_populates="sentence")


class SentenceWord(Base):
    __tablename__ = 'sentence_words'
    id = Column(Integer, primary_key=True, index=True)
    sentence_id = Column(Integer, ForeignKey('sentences.id'), nullable=False)
    word = Column(String(50), nullable=False)
    position = Column(Integer, nullable=False)

    sentence = relationship("Sentence", back_populates="words")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

class ImageChoice(Base):
    __tablename__ = 'image_choice_questions'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(255), nullable=False)
    correct_caption = Column(String(255), nullable=False)
    wrong_caption1 = Column(String(255), nullable=False)
    wrong_caption2 = Column(String(255), nullable=False)
    wrong_caption3 = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))  # Связь с таблицей категорий

    category = relationship('Category')

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
    seed_categories()
    seed_image_choice()
    seed_sentences_and_words()
    seed_notifications()
    initialize_ratings()


def initialize_ratings():
    """Добавление всех существующих пользователей в таблицу Rating с начальными значениями."""
    session = SessionLocal()

    try:
        # Получаем всех пользователей из таблицы User
        users = session.query(User).all()
        print(f"Найдено {len(users)} пользователей")

        for user in users:
            # Проверяем, есть ли у пользователя запись в таблице Rating
            existing_rating = session.query(Rating).filter(Rating.user_id == user.id).first()

            if not existing_rating:
                print(f"Создание рейтинга для пользователя с id {user.id}")
                new_rating = Rating(user_id=user.id)
                session.add(new_rating)
            else:
                print(f"Рейтинг для пользователя с id {user.id} уже существует")

        session.commit()
        print("Инициализация рейтингов завершена успешно")

    except IntegrityError as e:
        session.rollback()
        print(f"Ошибка при инициализации рейтингов: {e}")

    finally:
        session.close()

def seed_sentences_and_words():
    sentences = [
        # Уровень A1
        {"level_id": 1, "text": "The cat is on the table.",
         "words": ["cat", "is", "on", "the", "table", "dog", "car", "run"]},
        {"level_id": 1, "text": "I have a red apple.",
         "words": ["I", "have", "a", "red", "apple", "banana", "blue", "car"]},

        # Уровень A2
        {"level_id": 2, "text": "She likes to play tennis.",
         "words": ["She", "likes", "to", "play", "tennis", "soccer", "bike", "drive"]},
        {"level_id": 2, "text": "The weather is sunny today.",
         "words": ["The", "weather", "is", "sunny", "today", "cloudy", "rain", "snow"]},

        # Уровень B1
        {"level_id": 3, "text": "They went to the museum last weekend.",
         "words": ["They", "went", "to", "the", "museum", "last", "weekend", "beach", "yesterday"]},
        {"level_id": 3, "text": "He is learning how to cook Italian food.",
         "words": ["He", "is", "learning", "how", "to", "cook", "Italian", "food", "German", "paint"]},

        # Уровень B2
        {"level_id": 4, "text": "The economic situation is improving gradually.",
         "words": ["The", "economic", "situation", "is", "improving", "gradually", "suddenly", "worse", "quickly"]},
        {"level_id": 4, "text": "They decided to invest in renewable energy.",
         "words": ["They", "decided", "to", "invest", "in", "renewable", "energy", "fossil", "funds", "markets"]},

        # Уровень C1
        {"level_id": 5, "text": "The novel explores the complexities of human relationships.",
         "words": ["The", "novel", "explores", "the", "complexities", "of", "human", "relationships", "simple", "history"]},
        {"level_id": 5, "text": "His performance was lauded by critics and audiences alike.",
         "words": ["His", "performance", "was", "lauded", "by", "critics", "and", "audiences", "ignored", "friends", "enemies"]}
    ]

    session = SessionLocal()

    for sentence_data in sentences:
        # Проверяем, существует ли предложение
        existing_sentence = session.query(Sentence).filter_by(
            text=sentence_data["text"], level_id=sentence_data["level_id"]
        ).first()

        if existing_sentence:
            logging.info(f"Sentence already exists: {sentence_data['text']}")
            continue

        # Создаем новое предложение
        sentence = Sentence(text=sentence_data["text"], level_id=sentence_data["level_id"])

        try:
            # Сохранение предложения в базе данных
            session.add(sentence)
            session.commit()

            # Получение ID добавленного предложения
            sentence_id = sentence.id

            # Создание слов для предложения
            for position, word in enumerate(sentence_data["words"], start=1):
                sentence_word = SentenceWord(sentence_id=sentence_id, word=word, position=position)
                session.add(sentence_word)

            session.commit()

        except IntegrityError as e:
            session.rollback()
            logging.error(f"Ошибка при добавлении предложения: {e}")

    session.close()

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


def seed_notifications():
    notifications = [
        ("Welcome", "Thank you for using our application!"),
        ("Update Available", "A new update is available for download."),
        ("Maintenance", "Scheduled maintenance will occur tonight."),
    ]

    session = SessionLocal()
    for title, description in notifications:
        # Проверка наличия уведомления с таким заголовком
        existing_notification = session.query(Notification).filter_by(title=title).first()

        if existing_notification is None:
            # Уведомление не существует, добавляем новое
            notification = Notification(title=title, description=description)
            try:
                session.add(notification)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                logging.error(f"Failed to insert notification with title '{title}': {e}")
        else:
            logging.info(f"Notification with title '{title}' already exists.")

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

    def update_or_insert_rating(self, user_id, score, interval_key):
        """Обновляет или вставляет рейтинг пользователя для определенного временного интервала."""
        try:
            # Проверяем, есть ли уже рейтинг для этого пользователя
            existing_rating = self.session.query(Rating).filter_by(user_id=user_id).first()
            if existing_rating:
                # Если есть, обновляем только если новый результат лучше
                if score > getattr(existing_rating, interval_key):
                    setattr(existing_rating, interval_key, score)
                    self.session.commit()
            else:
                # Если нет, создаем новую запись
                new_rating_data = {
                    'user_id': user_id,
                    interval_key: score
                }
                new_rating = Rating(**new_rating_data)
                self.session.add(new_rating)
                self.session.commit()
            logging.debug(f"Rating for user {user_id} updated successfully")
            return True
        except IntegrityError as e:
            self.session.rollback()
            logging.error(f"Failed to update rating for user {user_id}: {e}")
            return False


    def get_random_images(self, category_id, limit=4):
        return (
            self.session.query(ImageChoice)
            .filter(ImageChoice.category_id == category_id)
            .order_by(func.random())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_sentence_words(sentence_id: int, db: Session):
        return db.query(SentenceWord).filter(SentenceWord.sentence_id == sentence_id).order_by(
            SentenceWord.position).all()

    @staticmethod
    def get_random_sentence(db: Session):
        return get_random_sentence(db)


    def get_random_question_with_answers(self):
        """Получает случайный вопрос с его вариантами ответов."""
        question = self.session.query(TestQuestion).order_by(func.random()).first()  # Получаем случайный вопрос
        if question:
            answers = self.session.query(TestAnswer).filter(TestAnswer.question_id == question.id).all()
            return question, answers
        return None, None

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

def get_random_sentence(db: Session):
    # Получаем все предложения
    sentences = db.query(Sentence).all()
    if sentences:
        # Выбираем случайное предложение
        return random.choice(sentences)
    return None

def seed_categories():
    categories = [
        (1, "trip"),
        (2, "hobby"),
        (3, "education"),
        (4, "art"),
        (5, "animals"),
        (6, "food")
    ]

    session = SessionLocal()
    for id, name in categories:
        # Использование merge для обновления существующих записей и добавления новых
        category = Category(id=id, name=name)
        try:
            session.merge(category)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            logging.error(f"Failed to insert or update category {id}: {e}")

    session.close()



def seed_image_choice():
    questions = [
        (1, "plane.png", "Plane", "Helicopter", "Hot Air Balloon", "Glider", 1),
        (2, "bus.png", "Bus", "Trolleybus", "Tram", "Minibus", 1),
        (3, "taxi.png", "Taxi", "Bus", "Fire truck", "Police car", 1),
        (4, "train.png", "Train", "Ship", "Submarine", "Truck", 1),
        (5, "helicopter.png", "Helicopter", "Plane", "Hot air balloon", "Paraglider", 1),
        (6, "bicycle.png", "Bicycle", "Scooter", "Motorcycle", "Skateboard", 1),
        (7, "motorboat.png", "Motorboat", "Train", "Tram", "Metro", 1),
        (8, "yacht.png", "Yacht", "Raft", "Cruise ship", "Submarine", 1),
        (9, "cruise-liner.png", "Cruise ship", "Raft", "Fishing boat", "Tanker", 1),
        (10, "watercraft.png", "Jet ski", "Catamaran", "Motorboat", "Paddleboard", 1),
        (11, "truck.png", "Long-distance truck", "Pickup Truck", "Van", "Sedan", 1),
        (12, "motorcycle.png", "Sport motorcycle", "Bicycle", "Scooter", "Segway", 1),
        (13, "Chess.png", "Chess", "Domino", "Crossword", "Sudoku", 2),
        (14, "Yoga.png", "Yoga", "Pilates", "Aerobics", "Tai Chi", 2),
        (15, "Painting on canvas.png", "Painting on canvas", "Embroidery", "Sculpture", "Photography", 2),
        (16, "Playing guitar.png", "Playing guitar", "Piano", "Drums", "Saxophone", 2),
        (17, "Photographer in nature.png", "Photographer in nature", "Cameraman", "Journalist", "Artist", 2),
        (18, "Gardening.png", "Gardening", "Fishing", "Hunting", "Swimming", 2),
        (19, "Fishing by river.png", "Fishing by river", "Hunting", "Gardening", "Tourism", 2),
        (20, "Reading a book.png", "Reading a book", "Writing", "Cooking", "Playing cards", 2),
        (21, "Running outdoors.png", "Running outdoors", "Walking", "Cycling", "Yoga", 2),
        (22, "Cooking food.png", "Cooking food", "Washing", "Cleaning", "Office work", 2),
        (23, "Rock climbing.png", "Rock climbing", "Hiking", "Surfing", "Skiing", 2),
        (24, "Dancing in studio.png", "Dancing in studio", "Gymnastics", "Fencing", "Boxing", 2),
        (25, "Textbook.png", "Textbook", "Notebook", "Atlas", "Magazine", 3),
        (26, "Classroom blackboard.png", "Classroom blackboard", "Screened monitor", "Mirror", "Window", 3),
        (27, "Chemistry laboratory.png", "Chemistry laboratory", "Library", "Classroom", "Cafe", 3),
        (28, "Reading in library.png", "Reading in library", "Cafe", "Office", "Classroom", 3),
        (29, "Computer lab.png", "Computer lab", "Sports hall", "Laboratory", "Art studio", 3),
        (30, "Student with textbooks.png", "Student with textbooks", "Student with dumbbells", "Student with tools", "Student with paints", 3),
        (31, "Taking an exam.png", "Taking an exam", "Sports competition", "Construction work", "Dance performance", 3),
        (32, "Attending lecture.png", "Attending lecture", "Watching a movie", "Meditation", "Music concert", 3),
        (33, "Student campus.png", "Student campus", "Office building", "Sports complex", "Residential area", 3),
        (34, "Globe.png", "Globe", "Gyroscope", "Moon model", "Telescope", 3),
        (35, "Diploma award.png", "Diploma award", "Theater performance", "Football match", "Concert", 3),
        (36, "Teacher in classroom.png", "Teacher in classroom", "Doctor in hospital", "Chef in kitchen", "Pilot in airplane", 3),
        (37, "Painting.png", "Painting", "Photography", "Engraving", "Sketch", 4),
        (38, "Marble sculpture.png", "Marble sculpture", "Painting", "Graffiti", "Fresco", 4),
        (39, "Artist's easel.png", "Artist's easel", "Book stand", "Table", "Drawing board", 4),
        (40, "Theater stage.png", "Theater stage", "Movie screen", "Art gallery", "Opera", 4),
        (41, "Ballet troupe.png", "Ballet troupe", "Football team", "Dance school", "Puppet theater", 4),
        (42, "Symphony orchestra.png", "Symphony orchestra", "Jazz band", "Rock band", "Quartet", 4),
        (43, "Ceramic vase.png", "Ceramic vase", "Glass bowl", "Wooden box", "Cardboard model", 4),
        (44, "Black-and-white photograph.png", "Black-and-white photograph", "Film", "Drawing", "Engraving", 4),
        (45, "Puppet show.png", "Puppet show", "Opera theater", "Circus performance", "Street concert", 4),
        (46, "Dance performance.png", "Dance performance", "Theater play", "Concert", "Film", 4),
        (47, "Street art.png", "Street art", "Advertisement", "Poster", "Drawing on paper", 4),
        (48, "Historical building.png", "Historical building", "Modern office", "Shopping center", "Stadium", 4),
        (49, "African lion.png", "African lion", "Tiger", "Leopard", "Cheetah", 5),
        (50, "Giant panda.png", "Giant panda", "Grizzly bear", "Koala", "Raccoon", 5),
        (51, "Ocean dolphin.png", "Ocean dolphin", "Whale", "Walrus", "Seal", 5),
        (52, "Antarctic penguin.png", "Antarctic penguin", "Seagull", "Albatross", "Pelican", 5),
        (53, "African elephant.png", "African elephant", "Rhinoceros", "Buffalo", "Hippo", 5),
        (54, "Giraffe in savannah.png", "Giraffe in savannah", "Zebra", "Llama", "Camel", 5),
        (55, "Grizzly bear.png", "Grizzly bear", "Koala", "Lemur", "Fox", 5),
        (56, "Orangutan in jungle.png", "Orangutan in jungle", "Gorilla", "Chimpanzee", "Baboon", 5),
        (57, "Goldfish.png", "Goldfish", "Crucian carp", "Cuttlefish", "Starfish", 5),
        (58, "Bald eagle.png", "Bald eagle", "Hawk", "Falcon", "Condor", 5),
        (59, "Gray wolf.png", "Gray wolf", "Jackal", "Coyote", "Fox", 5),
        (60, "Kangaroo in Australia.png", "Kangaroo in Australia", "Koala", "Lemur", "Opossum", 5),
        (61, "Italian pizza.png", "Italian pizza", "Pie", "Cake", "Lasagna", 6),
        (62, "Japanese sushi.png", "Japanese sushi", "Sashimi", "Rolls", "Maki", 6),
        (63, "Spaghetti with tomato sauce.png", "Spaghetti with tomato sauce", "Macaroni", "Noodles", "Ravioli", 6),
        (64, "Classic burger.png", "Classic burger", "Sandwich", "Taco", "Hot dog", 6),
        (65, "Fresh vegetable salad.png", "Fresh vegetable salad", "Fruit cocktail", "Casserole", "Omelette", 6),
        (66, "Chocolate cake.png", "Chocolate cake", "Honey cake", "Cheesecake", "Biscuit", 6),
        (67, "Omelette with herbs.png", "Omelette with herbs", "Hamburger", "Scrambled eggs", "Frittata", 6),
        (68, "Fruit smoothie.png", "Fruit smoothie", "Milkshake", "Compote", "Juice", 6),
        (69, "Apple pie.png", "Apple pie", "Muffin", "Croissant", "Cheesecake", 6),
        (70, "Cheese platter.png", "Cheese platter", "Fruit platter", "Meat platter", "Salad", 6),
    ]

    session = SessionLocal()

    for id, image_url, correct_caption, wrong_caption1, wrong_caption2, wrong_caption3, category_id in questions:
        try:
            image_choice_question = ImageChoice(
                id=id,
                image_url=image_url,
                correct_caption=correct_caption,
                wrong_caption1=wrong_caption1,
                wrong_caption2=wrong_caption2,
                wrong_caption3=wrong_caption3,
                category_id=category_id
            )
            session.merge(image_choice_question)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(f"Failed to insert or update ImageChoiceQuestion {id}: {e}")

    session.close()
