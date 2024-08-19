from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivy.core.window import Window
Window.size = (360, 640)
class SpecCard(MDCard):
    text = StringProperty('')  # Define the text property

class Example(MDApp):
    def build(self):
        kv = '''
<SpecCard>:
    md_bg_color: 255/255, 111/255, 97/255, 1
    padding: dp(15)
    ripple_behavior: True
    elevation: 2
    shadow_radius: 3
    orientation: 'vertical'

    MDLabel:
        text: root.text
        halign: 'center'
        valign: 'middle'
        size_hint_y: None
        height: self.texture_size[1]  # Height based on the text size

MDScreen:
    FloatLayout:
        SpecCard:
            size_hint: None, None
            size: dp(300), dp(50)  # Fixed size for each card
            pos_hint: {"center_x": 0.5, "center_y": 0.8}  # Position 1
            elevation: 4
            shadow_radius: 8
            text: "Card 1"
            on_press: print('11')

        SpecCard:
            size_hint: None, None
            size: dp(300), dp(50)  # Fixed size for each card
            pos_hint: {"center_x": 0.5, "center_y": 0.6}  # Position 2
            elevation: 4
            shadow_radius: 8
            text: "Card 2"

        SpecCard:
            size_hint: None, None
            size: dp(300), dp(50)  # Fixed size for each card
            pos_hint: {"center_x": 0.5, "center_y": 0.4}  # Position 3
            elevation: 4
            shadow_radius: 8
            text: "Card 3"

        SpecCard:
            size_hint: None, None
            size: dp(300), dp(50)  # Fixed size for each card
            pos_hint: {"center_x": 0.5, "center_y": 0.2}  # Position 4
            elevation: 4
            shadow_radius: 8
            text: "Card 4"
'''

        return Builder.load_string(kv)

Example().run()
