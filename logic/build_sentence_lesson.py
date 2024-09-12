import random
import string

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp, sp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from sqlalchemy.orm import Session, sessionmaker
from database.db import Database, engine  # Импортируйте вашу функцию
from gtts import gTTS
import pygame
from io import BytesIO

def speak_text(text):
    # Создание объекта gTTS
    tts = gTTS(text=text, lang='en', slow=False)

    # Используем BytesIO для создания виртуального файла
    virtual_file = BytesIO()
    tts.write_to_fp(virtual_file)
    virtual_file.seek(0)

    # Инициализация Pygame для проигрывания аудио
    pygame.mixer.init()
    pygame.mixer.music.load(virtual_file, "mp3")
    pygame.mixer.music.play()

    # Ожидание завершения воспроизведения
    while pygame.mixer.music.get_busy():
        continue

SessionLocal = sessionmaker(bind=engine)

class BuildSentenceLessonScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = SessionLocal()  # Создаем сессию базы данных
        self.original_sentence = []
        self.user_sentence = []
        self.next_button_mode = False
        self.load_new_sentence()  # Загружаем первое предложение

    def on_pre_enter(self, *args):
        # Загружаем новое предложение при входе на экран
        self.load_new_sentence()

    def get_random_sentence(self):
        return Database.get_random_sentence(self.db)

    def load_new_sentence(self):
        # Получаем новое предложение
        random_sentence = self.get_random_sentence()
        if random_sentence:
            self.sentence_id = random_sentence.id
            self.sentence_text = random_sentence.text  # Сохраняем текст предложения
            self.original_sentence = random_sentence.text.split()  # Сохраняем оригинальные слова предложения в список
            self.update_cards()  # Обновляем карточки

    def update_cards(self):
        words_list = [word.word for word in Database.get_sentence_words(self.sentence_id, self.db)]
        random.shuffle(words_list)  # Перемешиваем слова случайным образом

        # Очищаем контейнер перед добавлением новых элементов
        self.ids.cards_container.clear_widgets()
        self.ids.sentence_container.clear_widgets()  # Очищаем контейнер для предложения
        self.user_sentence = []  # Сбрасываем пользовательское предложение

        # Устанавливаем параметры GridLayout
        self.ids.cards_container.cols = 4  # Количество колонок
        self.ids.cards_container.spacing = dp(10)  # Пробел между карточками
        self.ids.cards_container.size_hint_y = None
        self.ids.cards_container.height = dp(50) * (
                    len(words_list) // self.ids.cards_container.cols)  # Устанавливаем начальную высоту контейнера

        for word in words_list:
            word_card = MDCard(
                size_hint=(None, None),  # Динамический размер
                width=self.calculate_card_width(word),
                height=dp(40),
                radius=[15, 15, 15, 15],
                elevation=1,
                on_release=lambda instance, word=word: self.add_to_sentence(instance, word),
                md_bg_color=[255/255, 223/255, 186/255, 1]
            )

            word_label = MDLabel(
                text=word,
                halign='center',
                valign='center',
                theme_text_color='Primary'
            )
            word_card.add_widget(word_label)

            # Добавляем карточку в контейнер
            self.ids.cards_container.add_widget(word_card)

        # Устанавливаем начальное состояние кнопки
        self.reset_button()

    def calculate_card_width(self, word):
        # Рассчитываем ширину карточки на основе длины слова
        base_width = dp(40)  # Базовая ширина карточки
        extra_width = sp(4) * len(word)  # Дополнительная ширина на основе длины слова
        return base_width + extra_width

    def add_to_sentence(self, instance, word):
        # Рассчитываем максимальную ширину
        max_width = dp(340)

        # Проверяем, существует ли текущий контейнер и достаточно ли в нем места
        if not hasattr(self, 'current_box_layout') or self.current_width + self.calculate_card_width(word) + dp(5) > max_width:
            # Создаем новый BoxLayout для новой строки
            self.current_box_layout = MDBoxLayout(
                orientation='horizontal',
                spacing=dp(5),
                size_hint_y=None,
                height=dp(40)
            )
            # Добавляем новый BoxLayout в вертикальный контейнер sentence_container
            self.ids.sentence_container.add_widget(self.current_box_layout)
            self.current_width = 0  # Сбрасываем ширину для новой строки

        # Создаем карточку для слова
        word_card = MDCard(
            size_hint=(None, None),  # Динамический размер
            width=self.calculate_card_width(word),
            height=dp(30),
            radius=[15, 15, 15, 15],
            elevation=1,
            on_release=lambda instance: self.remove_from_sentence(instance, word),
            md_bg_color=[1, 1, 1, 1]
        )

        word_label = MDLabel(
            text=word,
            halign='center',
            valign='center',
            theme_text_color='Primary'
        )
        word_card.add_widget(word_label)

        # Добавляем карточку в текущий BoxLayout
        self.current_box_layout.add_widget(word_card)
        self.current_width += word_card.width + dp(5)  # Обновляем текущую ширину

        # Добавляем слово в пользовательское предложение
        self.user_sentence.append(word.strip())

        # Скрыть карточку слова в списке
        instance.disabled = True

    def remove_from_sentence(self, instance, word):
        # Удаляем карточку из контейнера предложения
        parent_layout = instance.parent
        parent_layout.remove_widget(instance)

        # Если текущий BoxLayout пуст, удаляем его
        if len(parent_layout.children) == 0:
            self.ids.sentence_container.remove_widget(parent_layout)

        # Удаляем слово из пользовательского предложения
        if word in self.user_sentence:
            self.user_sentence.remove(word.strip())

        # Включаем карточку слова в списке
        for child in self.ids.cards_container.children:
            if child.children[0].text == word:  # Проверяем текст в MDLabel внутри MDCard
                child.disabled = False
                break

    def check_sentence(self):
        if not self.next_button_mode:  # Если кнопка в режиме "Перевірити"
            # Логика проверки предложения
            user_sentence_str = " ".join([word.lower().strip() for word in self.user_sentence])
            original_sentence_str = " ".join(
                [word.lower().strip().strip(string.punctuation) for word in self.original_sentence])

            user_sentence_str = user_sentence_str.translate(str.maketrans('', '', string.punctuation))

            print(f"User sentence: {user_sentence_str}")  # Отладочный вывод
            print(f"Original sentence: {original_sentence_str}")  # Отладочный вывод

            if user_sentence_str == original_sentence_str:
                self.set_button_state("success")
            else:
                self.set_button_state("error")
        else:
            # Если кнопка в режиме "Далі", вызываем следующий шаг
            self.next_step()

    def set_button_state(self, state):
        button = self.ids.check_buttn
        if state == "success":
            button.md_bg_color = [0, 1, 0, 1]  # Зеленый цвет
            button.children[0].text = "Далі"
        elif state == "error":
            button.md_bg_color = [1, 0, 0, 1]  # Красный цвет
            button.children[0].text = "Далі"

        self.next_button_mode = True  # Переключаем режим кнопки в "Далі"

    def reset_button(self):
        button = self.ids.check_buttn
        button.md_bg_color = [255 / 255, 223 / 255, 186 / 255, 1]  # Оригинальный цвет
        button.children[0].text = "Перевірити"
        self.next_button_mode = False  # Переключаем режим кнопки в "Перевірити"

    def next_step(self):
        # Обновляем предложение и карточки
        self.reset_button()
        self.load_new_sentence()

    def speak_sentence(self):
        # Воспроизводим предложение
        if hasattr(self, 'sentence_text'):
            speak_text(self.sentence_text)
