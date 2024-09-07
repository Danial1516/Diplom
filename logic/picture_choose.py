import random
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import ImageChoice

DATABASE_URL = "postgresql+psycopg2://qwe:qwe@localhost:5432/langvoyage"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class PictureChooseScreen(MDScreen):
    category = StringProperty()
    selected_card = None
    correct_card = None
    is_checked = False  # Флаг для блокировки выбора после проверки

    def on_pre_enter(self, *args):
        self.update_images()

    def on_leave(self, *args):
        # Сброс состояния при выходе с экрана
        self.reset_screen()

    def reset_screen(self):
        # Сбрасываем все состояния
        self.is_checked = False
        self.selected_card = None
        self.correct_card = None
        self.ids['check_button'].children[0].text = "Перевірити"
        self.ids['check_button'].md_bg_color = [255/255, 223/255, 186/255, 1]

        # Сбрасываем цвет всех карточек
        for card in ['card1', 'card2', 'card3', 'card4']:
            self.ids[card].md_bg_color = [240/255, 240/255, 240/255, 1]

    def update_images(self):
        session = SessionLocal()

        # Получаем все изображения для выбранной категории
        category_id = int(self.category)
        images = session.query(ImageChoice).filter(ImageChoice.category_id == category_id).all()

        if len(images) < 4:
            raise ValueError("Недостаточно изображений в выбранной категории")

        # Случайным образом выбираем 4 изображения
        selected_images = random.sample(images, 4)

        # Создаем словарь для подписей
        captions = {}
        correct_image = random.choice(selected_images)
        captions[correct_image.image_url] = correct_image.correct_caption

        # Сохраняем правильную карточку
        self.correct_card = correct_image.image_url

        # Для оставшихся изображений выбираем неправильные подписи
        for img in selected_images:
            if img != correct_image:
                wrong_captions = [img.wrong_caption1, img.wrong_caption2, img.wrong_caption3]
                random_wrong_caption = random.choice(wrong_captions)
                captions[img.image_url] = random_wrong_caption

        shuffled_images = list(captions.keys())
        random.shuffle(shuffled_images)

        image_sources = [f'assets/images/{img_url}' for img_url in shuffled_images]
        shuffled_captions = [captions[img_url] for img_url in shuffled_images]

        if len(shuffled_captions) != len(image_sources):
            raise ValueError("Количество подписей не совпадает с количеством изображений")

        image_ids = ['image1', 'image2', 'image3', 'image4']
        label_ids = ['label1', 'label2', 'label3', 'label4']

        # Обновляем карточки
        for i, image_id in enumerate(image_ids):
            if i < len(image_sources):
                self.ids.get(image_id).source = image_sources[i]

        for i, caption in enumerate(shuffled_captions):
            if i < len(label_ids):
                self.ids.get(label_ids[i]).text = caption

        session.close()

    def select_card(self, card_id):
        if self.is_checked:
            return  # Блокируем выбор после проверки

        if self.selected_card:
            self.ids[self.selected_card].md_bg_color = [240/255, 240/255, 240/255, 1]
        self.selected_card = card_id
        self.ids[card_id].md_bg_color = [173/255, 216/255, 230/255, 1]

    def check_selection(self):
        if not self.selected_card:
            return  # Если карточка не выбрана, ничего не делать

        self.is_checked = True  # Блокируем выбор после проверки

        selected_image_id = self.ids[self.selected_card].children[1].source.split('/')[-1]

        if selected_image_id == self.correct_card:
            self.ids[self.selected_card].md_bg_color = [0, 1, 0, 1]  # Зеленый цвет
            self.ids['check_button'].children[0].text = "Далі"
            self.ids['check_button'].md_bg_color = [0, 1, 0, 1]
        else:
            self.ids[self.selected_card].md_bg_color = [1, 0, 0, 1]  # Красный цвет
            for card in ['card1', 'card2', 'card3', 'card4']:
                if self.correct_card in self.ids[card].children[1].source:
                    self.ids[card].md_bg_color = [0, 1, 0, 1]
                    break
            self.ids['check_button'].children[0].text = "Далі"
            self.ids['check_button'].md_bg_color = [1, 0, 0, 1]

    def next_round(self):
        self.is_checked = False
        self.selected_card = None
        self.correct_card = None
        self.ids['check_button'].children[0].text = "Перевірити"
        self.ids['check_button'].md_bg_color = [255/255, 223/255, 186/255, 1]

        for card in ['card1', 'card2', 'card3', 'card4']:
            self.ids[card].md_bg_color = [240/255, 240/255, 240/255, 1]

        self.update_images()
