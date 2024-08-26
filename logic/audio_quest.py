from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, DictProperty

class AudioQuestionsScreen(MDScreen):
    selected_option = StringProperty('')

    def select_option(self, option, question_id):
        self.ids[f'true_option_{question_id}'].md_bg_color = [255 / 255, 255 / 255, 255 / 255, 1]
        self.ids[f'false_option_{question_id}'].md_bg_color = [255 / 255, 255 / 255, 255 / 255, 1]

        if option == 'true':
            self.ids[f'true_option_{question_id}'].md_bg_color = [173 / 255, 216 / 255, 230 / 255, 1]
        elif option == 'false':
            self.ids[f'false_option_{question_id}'].md_bg_color = [173 / 255, 216 / 255, 230 / 255, 1]

        self.selected_option = option

    selected_options = DictProperty({})  # Словарь для хранения выбранных вариантов для каждого вопроса

    def select_fill_in_the_blanks_option(self, option_id):
        # Определяем вопрос по option_id
        question_id = option_id.split('_')[2]  # Например, если option_id = 'option_1_q1', question_id = 'q1'

        # Проверяем, был ли уже выбран вариант для этого вопроса, если да, сбрасываем его подсветку
        previous_selected_option = self.selected_options.get(question_id)
        if previous_selected_option:
            self.ids[previous_selected_option].md_bg_color = [255 / 255, 255 / 255, 255 / 255, 1]  # Сброс подсветки

        # Подсвечиваем новый выбранный вариант
        self.ids[option_id].md_bg_color = [173 / 255, 216 / 255, 230 / 255, 1]

        # Обновляем словарь с выбранным вариантом для этого вопроса
        self.selected_options[question_id] = option_id
