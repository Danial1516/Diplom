from kivy.properties import ObjectProperty, Clock
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from database.db import Database

class TimeTestQuestions(MDScreen):
    timer_event = None
    remaining_time = 0  # Оставшееся время в секундах
    db = Database()
    used_question_ids = set()

    def on_pre_enter(self, *args):
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

        # Проверяем, что вопрос и ответы существуют и что вопрос еще не использовался
        if question and question.id not in self.used_question_ids:
            self.used_question_ids.add(question.id)  # Добавляем вопрос в список использованных

            # Обновляем текст вопроса
            self.ids.question_label.text = question.text

            # Обновляем варианты ответов
            self.ids.option_1.children[0].text = answers[0].first_option
            self.ids.option_2.children[0].text = answers[0].second_option
            self.ids.option_3.children[0].text = answers[0].third_option

            # Связываем событие выбора ответа с методом обработки
            self.ids.option_1.on_release = lambda: self.on_answer_selected(answers[0].first_option,
                                                                           answers[0].is_correct)
            self.ids.option_2.on_release = lambda: self.on_answer_selected(answers[0].second_option,
                                                                           answers[0].is_correct)
            self.ids.option_3.on_release = lambda: self.on_answer_selected(answers[0].third_option,
                                                                           answers[0].is_correct)

    def on_answer_selected(self, selected_answer, correct_answer):
        """Обрабатывает выбор ответа пользователем."""
        if selected_answer == correct_answer:
            print("Correct!")
        else:
            print("Incorrect!")

        # Загружаем новый вопрос после выбора ответа
        self.load_new_question()

    def parse_time_to_seconds(self, time_str):
        """Преобразует строку времени в секунды."""
        if 'секунд' in time_str:
            return int(time_str.split()[0])
        elif 'хвилина' in time_str:
            return int(time_str.split()[0]) * 60
        elif 'хвилини' in time_str:
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

    def update_timer_label(self):
        """Обновляет метку с оставшимся временем."""
        minutes, seconds = divmod(self.remaining_time, 60)
        self.ids.timer_label.text = f"{minutes:02}:{seconds:02}"

    def on_leave(self, *args):
        """Сброс таймера при выходе с экрана."""
        if self.timer_event:
            self.timer_event.cancel()
        self.ids.timer_label.text = "00:00"