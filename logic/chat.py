from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty
from kivy.core.text import LabelBase

import json
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

# Загрузка модели и эмбеддингов
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
question_embeddings = torch.load('question_embeddings.pt')

# Чтение данных из файла
with open('qust_expanded.txt', 'r', encoding='utf-8') as file:
    data = json.load(file)
df = pd.DataFrame(data)
answers = df['answer'].tolist()

def find_best_answer(question, model, question_embeddings, answers, threshold=0.7):
    # Создание эмбеддинга для нового вопроса
    question_embedding = model.encode(question, convert_to_tensor=True)
    # Поиск схожести между новым вопросом и вопросами из базы данных
    similarities = util.pytorch_cos_sim(question_embedding, question_embeddings)[0]
    # Индекс наиболее похожего вопроса
    most_similar_index = similarities.argmax().item()
    # Значение схожести для наиболее близкого вопроса
    similarity_score = similarities[most_similar_index].item()
    # Проверяем, превышает ли схожесть заданный порог
    if similarity_score < threshold:
        return "Вопрос не найден, попробуйте переформулировать."
    # Возвращаем ответ для наиболее похожего вопроса
    return answers[most_similar_index], similarity_score

class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Clearsan"
    font_size = 17

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_name = "Clearsan"
    font_size = 17

class ResponseImage(Image):
    source = StringProperty()

class ChatScreen(MDScreen):
    def bot_name(self):
        if self.ids.bot_name.text != "":
            self.ids.bot_name.text = self.ids.bot_name.text

    def response(self, *args):
        user_message = self.value
        answer, score = find_best_answer(user_message, model, question_embeddings, answers)
        self.ids.chat_list.add_widget(Response(text=answer, size_hint_x=.75))

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
