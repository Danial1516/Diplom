from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp, sp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.core.window import Window


class BuildSentenceLessonScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_cards(["I", "want", "a", "salad", "glass", "without", "juice", "orange", "water"])

    def update_cards(self, words_list):
        # Очищаем контейнер перед добавлением новых элементов
        self.ids.cards_container.clear_widgets()

        # Устанавливаем параметры GridLayout
        self.ids.cards_container.cols = 4  # Количество колонок
        self.ids.cards_container.spacing = dp(10)  # Пробел между карточками
        self.ids.cards_container.size_hint_y = None
        self.ids.cards_container.height = dp(50) * (len(words_list) // self.ids.cards_container.cols)  # Устанавливаем начальную высоту контейнера

        for word in words_list:
            word_card = MDCard(
                size_hint=(None, None),  # Динамический размер
                width=self.calculate_card_width(word),
                height=dp(40),
                radius=[15, 15, 15, 15],
                elevation=1,
                on_release=lambda instance, word=word: self.add_to_sentence(instance, word),
                md_bg_color=[1, 1, 1, 1]
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

    def calculate_card_width(self, word):
        # Рассчитываем ширину карточки на основе длины слова
        base_width = dp(40)  # Базовая ширина карточки
        extra_width = sp(4) * len(word)  # Дополнительная ширина на основе длины слова
        return base_width + extra_width

    def add_to_sentence(self, instance, word):
        # Рассчитываем максимальную ширину
        max_width = dp(310)

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

        # Скрыть карточку слова в списке
        instance.disabled = True

    def remove_from_sentence(self, instance, word):
        # Удаляем карточку из контейнера предложения
        parent_layout = instance.parent
        parent_layout.remove_widget(instance)

        # Если текущий BoxLayout пуст, удаляем его
        if len(parent_layout.children) == 0:
            self.ids.sentence_container.remove_widget(parent_layout)

        # Включаем карточку слова в списке
        for child in self.ids.cards_container.children:
            if child.children[0].text == word:  # Проверяем текст в MDLabel внутри MDCard
                child.disabled = False
                break
