# logic/chat.py

from kivymd.uix.label import MDLabel

def show_greeting(app):
    chat_list = app.root.get_screen('chat').ids.chat_list
    chat_list.add_widget(MDLabel(text="Привіт! Я помічник LangVoyage. Готовий допомогти тобі з будь-якими питаннями. Обери тему, що цікавить, нижче, і ми почнемо! 😊", halign='center'))

def show_translation(app):
    chat_list = app.root.get_screen('chat').ids.chat_list
    chat_list.add_widget(MDLabel(text="Введіть текст для перекладу", halign='center'))
    # Логика для ввода текста и получения перевода

def show_lexicon(app):
    # Логика для отображения "Лексика за темами"
    pass

def show_grammar(app):
    # Логика для отображения "Граматика"
    pass

def show_phonetics(app):
    # Логика для отображения "Фонетика"
    pass
