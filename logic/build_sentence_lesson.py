from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel


class CustMDCard(MDBoxLayout):
    pass


class BuildSentenceLessonScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_cards(["word1", "word2", "wo1244rd3", "word4",  "word4",  "word4",  "word4"])  # Замените на ваш список слов

    def update_cards(self, words_list):
        # Удаляем все предыдущие элементы, чтобы начать заново
        self.ids.cards_container.clear_widgets()

        # Переменная для текущего MDBoxLayout
        current_box_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(40))
        self.ids.cards_container.add_widget(current_box_layout)

        for i, word in enumerate(words_list):
            if i > 0 and i % 3 == 0:
                # Если 3 слова уже добавлены, создаем новый MDBoxLayout
                current_box_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None,
                                                 height=dp(40))
                self.ids.cards_container.add_widget(current_box_layout)

            # Создаем CustMDCard с MDCard внутри
            cust_md_card = CustMDCard()
            card = MDCard(size_hint_x=0.5, md_bg_color=[1, 1, 1, 1], radius=[15, 15, 15, 15], elevation=1)

            card.add_widget(MDLabel(
                text=word,
                font_name="juneg",
                halign="center",
                valign="center",
                theme_text_color="Primary"
            ))

            cust_md_card.add_widget(card)
            current_box_layout.add_widget(cust_md_card)
