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

    def on_pre_enter(self, *args):
        self.update_images()

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

        # Для оставшихся изображений выбираем неправильные подписи
        for img in selected_images:
            if img != correct_image:
                # Найти неправильные подписи для текущего изображения
                wrong_captions = [img.wrong_caption1, img.wrong_caption2, img.wrong_caption3]
                # Выбираем случайную неправильную подпись
                random_wrong_caption = random.choice(wrong_captions)
                captions[img.image_url] = random_wrong_caption

        # Перемешиваем изображения и подписи
        shuffled_images = list(captions.keys())
        random.shuffle(shuffled_images)

        # Устанавливаем пути к изображениям и подписи
        image_sources = [f'assets/images/{img_url}' for img_url in shuffled_images]
        shuffled_captions = [captions[img_url] for img_url in shuffled_images]

        # Убедимся, что список подписей и источников изображений совпадают по длине
        if len(shuffled_captions) != len(image_sources):
            raise ValueError("Количество подписей не совпадает с количеством изображений")

        image_ids = ['image1', 'image2', 'image3', 'image4']
        label_ids = ['label1', 'label2', 'label3', 'label4']

        # Обновляем карточки
        for i, image_id in enumerate(image_ids):
            if i < len(image_sources):
                # Обновляем источник изображения
                self.ids.get(image_id).source = image_sources[i]

        # Обновляем тексты на метках
        for i, caption in enumerate(shuffled_captions):
            if i < len(label_ids):
                self.ids.get(label_ids[i]).text = caption

        session.close()
