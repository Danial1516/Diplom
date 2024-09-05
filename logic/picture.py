from kivymd.uix.screen import MDScreen


class PictureScreen(MDScreen):
    def set_category(self, category_name):
        # Сохраняем выбранную категорию в 'PictureChooseScreen'
        picture_choose_screen = self.manager.get_screen('picture_choose_screen')
        picture_choose_screen.category = category_name
        # Переключаемся на следующий экран
        self.manager.current = 'picture_choose_screen'