from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class WrapLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = kwargs.get('spacing', 10)
        self._update_layout()

    def on_size(self, *args):
        self._update_layout()

    def _update_layout(self):
        xpos = 0
        ypos = 0
        row_height = 0

        for child in self.children:
            child_width = child.width
            child_height = child.height

            if xpos + child_width > self.width:
                xpos = 0
                ypos += row_height
                row_height = 0

            child.pos = (xpos, ypos)
            xpos += child_width + self.spacing
            row_height = max(row_height, child_height)

        self.height = ypos + row_height

class CustMDCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.words = kwargs.get('words', [])

    def update_words(self):
        words_box = self.ids.words_box
        words_box.clear_widgets()

        for word in self.words:
            card = MDCard(
                size_hint_x=None,
                width="150dp",
                md_bg_color=[255/255, 255/255, 255/255, 1],
                radius=[15, 15, 15, 15],
                elevation=1,
            )

            card_label = MDLabel(
                text=word,
                font_name="juneg",
                halign="center",
                valign="center",
                theme_text_color="Primary",
            )

            card.add_widget(card_label)
            words_box.add_widget(card)

class BuildSentenceLessonScreen(MDScreen):
    pass