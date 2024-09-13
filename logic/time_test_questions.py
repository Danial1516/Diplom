from kivy.properties import ObjectProperty, Clock, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from database.db import Database


class CustomDialCont(MDBoxLayout):
    pass


class TimeTestQuestions(MDScreen):
    timer_event = None
    remaining_time = 0  # Оставшееся время в секундах
    correct_answers = NumericProperty(0)  # Количество правильных ответов
    total_questions = NumericProperty(0)  # Общее количество вопросов
    consecutive_correct_answers = NumericProperty(0)  # Текущие правильные ответы подряд
    total_consecutive_correct_answers = NumericProperty(0)  # Суммарные правильные ответы подряд
    total_remaining_time = NumericProperty(0)  # Накопленное время для бонуса
    db = Database()
    used_question_ids = set()

    def on_pre_enter(self, *args):
        self.correct_answers = 0
        self.total_questions = 0
        self.consecutive_correct_answers = 0
        self.total_consecutive_correct_answers = 0
        self.total_remaining_time = 0
        self.used_question_ids.clear()

        self.load_new_question()
        time_test_screen = self.manager.get_screen('time_test')
        selected_time = time_test_screen.selected_time  # Получаем выбранное время

        # Преобразование времени в секунды
        self.remaining_time = self.parse_time_to_seconds(selected_time)

        # Сброс таймера
        if self.timer_event:
            self.timer_event.cancel()
        self.start_timer()

    def load_new_question(self):
        """Загружает новый вопрос и ответы, обновляет интерфейс."""
        question, answers = self.db.get_random_question_with_answers()

        # Переменная для хранения следующего вопроса
        next_question = None

        # Ищем вопрос, который не был использован
        while next_question is None:
            if question and question.id not in self.used_question_ids:
                next_question = question
                self.used_question_ids.add(question.id)  # Добавляем вопрос в список использованных
                self.total_questions += 1  # Увеличиваем счетчик вопросов
            else:
                # Получаем следующий вопрос
                question, answers = self.db.get_random_question_with_answers()

        # Обновляем текст вопроса
        self.ids.question_label.text = next_question.text

        # Обновляем варианты ответов
        self.ids.option_1.children[0].text = answers[0].first_option
        self.ids.option_2.children[0].text = answers[0].second_option
        self.ids.option_3.children[0].text = answers[0].third_option

        # Связываем событие выбора ответа с методом обработки
        self.ids.option_1.on_release = lambda: self.on_answer_selected(answers[0].first_option, answers[0].is_correct)
        self.ids.option_2.on_release = lambda: self.on_answer_selected(answers[0].second_option, answers[0].is_correct)
        self.ids.option_3.on_release = lambda: self.on_answer_selected(answers[0].third_option, answers[0].is_correct)

    def on_answer_selected(self, selected_answer, correct_answer):
        """Обрабатывает выбор ответа пользователем."""
        if selected_answer == correct_answer:
            self.correct_answers += 1
            self.consecutive_correct_answers += 1  # Увеличиваем количество правильных ответов подряд
            self.total_remaining_time += self.remaining_time * 0.1  # Учитываем бонусное время
            print("Correct!")
        else:
            # Сохраняем количество правильных ответов подряд, если их больше 1
            if self.consecutive_correct_answers > 1:
                self.total_consecutive_correct_answers += self.consecutive_correct_answers
            self.consecutive_correct_answers = 0  # Сброс текущего количества правильных ответов подряд
            print("Incorrect!")

        # Загружаем новый вопрос после выбора ответа
        self.load_new_question()

    def parse_time_to_seconds(self, time_str):
        """Преобразует строку времени в секунды."""
        if 'секунд' in time_str:
            return int(time_str.split()[0])
        elif 'хвилина' in time_str or 'хвилини' in time_str:
            return int(time_str.split()[0]) * 60
        return 0  # Возвращает 0, если формат времени не распознан

    def start_timer(self):
        """Запуск таймера с обновлением каждую секунду."""
        self.update_timer_label()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        """Обновляет оставшееся время и метку таймера каждую секунду."""
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_timer_label()
        else:
            self.timer_event.cancel()  # Остановка таймера, когда он заканчивается
            self.show_results_dialog()

    def update_timer_label(self):
        """Обновляет метку с оставшимся временем."""
        minutes, seconds = divmod(self.remaining_time, 60)
        self.ids.timer_label.text = f"{minutes:02}:{seconds:02}"

    def show_results_dialog(self):
        """Отображает диалог с результатами."""
        # Учитываем оставшиеся правильные ответы подряд, если больше 1
        if self.consecutive_correct_answers > 1:
            self.total_consecutive_correct_answers += self.consecutive_correct_answers

        # Рассчитываем баллы
        score = self.calculate_score()

        content = CustomDialCont()
        content.ids.score_label.text = (
            f"Правильних відповідей {self.correct_answers} з {self.total_questions}\n"
            f"Ваші бали: {score:.2f}"
        )

        self.dialog = MDDialog(
            title="Результат",
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

    def calculate_score(self):
        """Вычисляет окончательный счёт пользователя."""
        return (
            self.correct_answers * 10 +  # Базовые баллы за правильные ответы
            self.total_consecutive_correct_answers * 10 +  # Бонус за правильные ответы подряд
            self.total_remaining_time  # Бонусное время
        )

    def on_dialog_ok(self, *args):
        """Закрывает диалог и возвращает пользователя на экран 'time_test'."""
        self.dialog.dismiss()
        self.manager.current = 'time_test'

    def reset_test_state(self):
        """Сбрасывает состояние теста."""
        self.correct_answers = 0
        self.total_questions = 0
        self.used_question_ids.clear()

    def on_leave(self, *args):
        """Сброс таймера при выходе с экрана."""
        if self.timer_event:
            self.timer_event.cancel()
        self.ids.timer_label.text = "00:00"
