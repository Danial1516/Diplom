from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty

class AudioQuestionsScreen(MDScreen):
    selected_option = StringProperty('')  # Для хранения выбранного варианта

    def select_option(self, option, question_id):
        # Убираем подсветку со всех вариантов для данного вопроса
        self.ids[f'true_option_{question_id}'].md_bg_color = [255 / 255, 255 / 255, 255 / 255, 1]
        self.ids[f'false_option_{question_id}'].md_bg_color = [255 / 255, 255 / 255, 255 / 255, 1]

        # Подсвечиваем выбранный вариант для текущего вопроса
        if option == 'true':
            self.ids[f'true_option_{question_id}'].md_bg_color = [173 / 255, 216 / 255, 230 / 255,
                                                                  1]  # Цвет для подсветки
        elif option == 'false':
            self.ids[f'false_option_{question_id}'].md_bg_color = [173 / 255, 216 / 255, 230 / 255,
                                                                   1]  # Цвет для подсветки

        # Сохраняем выбранный вариант
        self.selected_option = option

