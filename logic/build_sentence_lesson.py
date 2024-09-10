from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp, sp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.core.window import Window


class CustMDCard(MDBoxLayout):
    pass


class BuildSentenceLessonScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_cards(["I", "want", "a", "salad", "glass", "without", "juice", "orange", "water"])  # Ваш список слов

    def update_cards(self, words_list):
        # Очищаем контейнер перед добавлением новых элементов
        self.ids.cards_container.clear_widgets()

        # Начальный контейнер для слов
        current_box_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=self.ids.cards_container.minimum_height,
            adaptive_height=True
        )

        self.ids.cards_container.add_widget(current_box_layout)

        total_width = 0  # Общая ширина для текущей строки
        max_width = Window.width - dp(40)  # Максимальная ширина строки (размер окна - отступы)

        for word in words_list:
            # Создаем карточку для каждого слова
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

            # Если добавление карточки превышает ширину контейнера, создаем новый MDBoxLayout
            if total_width + word_card.width > max_width:
                current_box_layout = MDBoxLayout(
                    orientation='horizontal',
                    spacing=dp(10),
                    size_hint_y=None,
                    height=self.ids.cards_container.minimum_height,
                    adaptive_height=True
                )
                self.ids.cards_container.add_widget(current_box_layout)
                total_width = 0  # Сбрасываем ширину для новой строки

            # Добавляем карточку в текущий контейнер
            current_box_layout.add_widget(word_card)
            total_width += word_card.width + dp(10)  # Обновляем общую ширину строки

    def calculate_card_width(self, word):
        # Рассчитываем ширину карточки на основе длины слова
        base_width = dp(50)  # Базовая ширина карточки
        extra_width = sp(8) * len(word)  # Дополнительная ширина на основе длины слова
        return base_width + extra_width

    def add_to_sentence(self, instance, word):
        # Добавляем слово в контейнер предложения
        word_card = MDCard(
            size_hint=(None, None),  # Динамический размер
            width=self.calculate_card_width(word),
            height=dp(40),
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

        # Скрыть карточку слова в списке
        instance.disabled = True
        self.ids.sentence_container.add_widget(word_card)

    def remove_from_sentence(self, instance, word):
        # Удаляем слово из предложения
        self.ids.sentence_container.remove_widget(instance)

        # Включаем карточку слова в списке
        for child in self.ids.cards_container.children:
            for card in child.children:
                if card.children[0].text == word:  # Проверяем текст в MDLabel внутри MDCard
                    card.disabled = False
                    break
