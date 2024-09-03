from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.db import TestQuestion, TestAnswer


# Настройка подключения к базе данных
DATABASE_URL = "postgresql+psycopg2://qwe:qwe@localhost:5432/langvoyage"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class CustomDialogContent(BoxLayout):
    pass

class CustomMDCard(MDCard):
    question_label = StringProperty("Question")
    option_1 = StringProperty("Option 1")
    option_2 = StringProperty("Option 2")
    option_3 = StringProperty("Option 3")
    selected_answer = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.option_buttons = []

    def on_option_button_release(self, instance):
        option_text = instance.children[0].text  # MDLabel является единственным дочерним виджетом MDCard
        self.selected_answer = option_text
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
        self.minutes = 20
        self.dialog = None
        self.timer_event = None

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

    def on_dialog_ok(self, instance):
        self.dialog.dismiss()
        # Измените текущий экран на 'testing'
        self.manager.current = 'testing'

    def check_user_answers(self):
        """
        Функция для проверки ответов пользователя.
        """
        session = SessionLocal()
        correct_counts = {"A1-A2": 0, "B1-B2": 0, "C1": 0}  # Счетчики правильных ответов по уровням

        try:
            # Получаем правильные ответы из базы данных
            questions = session.query(TestQuestion).filter(TestQuestion.level_id.in_([2, 4, 5])).all()
            for question in questions:
                correct_answer = session.query(TestAnswer).filter(TestAnswer.question_id == question.id).first()

                if correct_answer:
                    # Находим соответствующую карточку с вопросом
                    card = next(
                        (card for card in self.ids.card_container.children if card.question_label == question.text),
                        None)

                    if card and card.selected_answer == correct_answer.is_correct:
                        # Увеличиваем счетчик правильных ответов по соответствующему уровню
                        if question.level_id == 2:
                            correct_counts["A1-A2"] += 1
                        elif question.level_id == 4:
                            correct_counts["B1-B2"] += 1
                        elif question.level_id == 5:
                            correct_counts["C1"] += 1

        except Exception as e:
            print(f"Error checking user answers: {e}")
        finally:
            session.close()

        return correct_counts

    def calculate_knowledge_level(self, correct_counts):
        """
        Рассчитывает уровень знаний пользователя на основе правильных ответов.
        """
        # Количество вопросов для каждого уровня
        total_questions = {"A1-A2": 14, "B1-B2": 12, "C1": 9}
        # Весовые коэффициенты для каждого уровня
        weights = {"A1-A2": 1, "B1-B2": 2, "C1": 3}

        # Рассчитываем общий балл пользователя
        score = (
                (correct_counts["A1-A2"] / total_questions["A1-A2"]) * weights["A1-A2"] +
                (correct_counts["B1-B2"] / total_questions["B1-B2"]) * weights["B1-B2"] +
                (correct_counts["C1"] / total_questions["C1"]) * weights["C1"]
        )

        # Определяем уровень пользователя на основе общего балла
        if score < 1.8:
            return "A1"
        elif score < 3.2:
            return "A2"
        elif score < 4.6:
            return "B1"
        elif score < 5.2:
            return "B2"
        else:
            return "C1"

    def show_results_dialog(self):
        correct_counts = self.check_user_answers()
        level = self.calculate_knowledge_level(correct_counts)
        correct_answers_total = sum(correct_counts.values())
        # Проверяем, если диалог уже существует
        if not self.dialog:
            # Создаем кастомное содержимое диалога
            content = CustomDialogContent()

            # Устанавливаем текст уровней и количества правильных ответов
            content.ids.level_label.text = f"Рівень: {level}"
            content.ids.score_label.text = f"Правильних відповідей: {correct_answers_total} з 35"

            # Создаем диалог
            self.dialog = MDDialog(
                title="Результат тестування",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.on_dialog_ok
                    ),
                ],
            )
        self.dialog.open()

    def on_enter(self):
        # Запуск обновления таймера каждую секунду при входе на экран
        self.reset_timer()  # Сброс таймера
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def on_leave(self):
        # Остановка таймера при выходе с экрана
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        self.reset_timer()  # Сброс таймера

    def reset_timer(self):
        # Сброс таймера
        self.seconds = 0
        self.minutes = 20
        self.ids.timer_label.text = f"{self.minutes:02}:{self.seconds:02}"

    def on_timer_finished(self):
        # Логика для завершения таймера
        self.show_results_dialog()

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