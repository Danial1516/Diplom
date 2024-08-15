from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty
from kivy.core.text import LabelBase

class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Poppins"
    font_size = 17

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Poppins"
    font_size = 17

class ResponseImage(Image):
    source = StringProperty()

class ChatScreen(MDScreen):
    def bot_name(self):
        if self.ids.bot_name.text != "":
            self.ids.bot_name.text = self.ids.bot_name.text

    def response(self, *args):
        response = ""
        if self.value == "Hello" or self.value == "hello":
            response = f"Hello. I Am Your Personal Assistant."
        elif self.value == "How are you?" or self.value == "how are you?":
            response = "I'm doing well. Thanks!"
        elif self.value == "Images":
            self.ids.chat_list.add_widget(ResponseImage(source="chatbots.jpg"))
        elif self.value == "Images1":
            self.ids.chat_list.add_widget(ResponseImage(source="1.png"))
        else:
            response = "Sorry could you say that again?"
        self.ids.chat_list.add_widget(Response(text=response, size_hint_x=.75))

    def send(self):
        if self.ids.text_input.text != "":
            self.value = self.ids.text_input.text
            if len(self.value) < 6:
                size = .22
                halign = "center"
            elif len(self.value) < 11:
                size = .32
                halign = "center"
            elif len(self.value) < 16:
                size = .45
                halign = "center"
            elif len(self.value) < 21:
                size = .58
                halign = "center"
            elif len(self.value) < 26:
                size = .71
                halign = "center"
            else:
                size = .77
                halign = "left"
            self.ids.chat_list.add_widget(
                Command(text=self.value, size_hint_x=size, halign=halign))
            Clock.schedule_once(self.response, 2)
            self.ids.text_input.text = ""

