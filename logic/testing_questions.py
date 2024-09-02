from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.db import TestQuestion, TestAnswer


# Настройка подключения к базе данных
DATABASE_URL = "postgresql+psycopg2://qwe:qwe@localhost:5432/langvoyage"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CustomMDCard(MDCard):
    question_label = StringProperty("Question")
    option_1 = StringProperty("Option 1")
    option_2 = StringProperty("Option 2")
    option_3 = StringProperty("Option 3")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.option_buttons = []

    def on_option_button_release(self, instance):
        self._update_selection(instance)

    def _update_selection(self, selected_button):
        for button in self.option_buttons:
            if button != selected_button:
                button.md_bg_color = [255 / 255, 255 / 255, 255 / 255, 1]  # Unselected color
            else:
                button.md_bg_color = [173 / 255, 216 / 255, 230 / 255, 1]  # Selected color


class TestingQuestions(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seconds = 0
        self.minutes = 20  # Установить таймер на 20 минут
        # Запуск обновления таймера каждую секунду
        Clock.schedule_interval(self.update_timer, 1)

        # Получение вопросов из базы данных
        questions = self.fetch_questions_and_answers()

        # Получаем ссылку на MDBoxLayout
        card_container = self.ids.card_container

        # Создаем карточки и добавляем их в layout
        for q in questions:
            card = CustomMDCard()
            card.question_label = q["question"]
            card.option_1 = q["options"][0]
            card.option_2 = q["options"][1]
            card.option_3 = q["options"][2]

            # Инициализация кнопок
            card.option_buttons = [
                card.ids.option_1,
                card.ids.option_2,
                card.ids.option_3
            ]

            # Подписка на события нажатий
            for button in card.option_buttons:
                button.bind(on_release=card.on_option_button_release)

            card_container.add_widget(card)

    def fetch_questions_and_answers(self):
        """
        Функция для получения вопросов и вариантов ответов из базы данных.
        """
        session = SessionLocal()
        questions_with_answers = []

        try:
            # Запрос вопросов уровня A1-A2, B1-B2, C1
            questions = session.query(TestQuestion).filter(TestQuestion.level_id.in_([2, 4, 5])).all()

            for question in questions:
                # Запрос ответов на каждый вопрос
                answers = session.query(TestAnswer).filter(TestAnswer.question_id == question.id).first()

                if answers:
                    questions_with_answers.append({
                        "question": question.text,
                        "options": [answers.first_option, answers.second_option, answers.third_option]
                    })

        except Exception as e:
            print(f"Error fetching questions and answers: {e}")
        finally:
            session.close()

        return questions_with_answers

    def update_timer(self, dt):
        # Логика для обратного отсчета таймера
        if self.seconds == 0:
            if self.minutes == 0:
                # Таймер завершен, можно выполнить действие
                Clock.unschedule(self.update_timer)
                self.on_timer_finished()
                return
            else:
                self.minutes -= 1
                self.seconds = 59
        else:
            self.seconds -= 1

        # Обновляем текст таймера
        self.ids.timer_label.text = f"{self.minutes:02}:{self.seconds:02}"