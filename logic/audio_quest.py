import os

from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, DictProperty

class AudioQuestionsScreen(MDScreen):
    selected_option = StringProperty('')

    # Свойства для хранения данных из словаря
    t_f_q1 = StringProperty('')
    t_f_q2 = StringProperty('')
    t_f_q3 = StringProperty('')
    t_f_q4 = StringProperty('')
    t_f_q5 = StringProperty('')

    q1 = StringProperty('')
    q2 = StringProperty('')
    q3 = StringProperty('')
    q4 = StringProperty('')
    q5 = StringProperty('')

    q1_op1 = StringProperty('')
    q1_op2 = StringProperty('')
    q1_op3 = StringProperty('')
    q2_op1 = StringProperty('')
    q2_op2 = StringProperty('')
    q2_op3 = StringProperty('')
    q3_op1 = StringProperty('')
    q3_op2 = StringProperty('')
    q3_op3 = StringProperty('')
    q4_op1 = StringProperty('')
    q4_op2 = StringProperty('')
    q4_op3 = StringProperty('')
    q5_op1 = StringProperty('')
    q5_op2 = StringProperty('')
    q5_op3 = StringProperty('')

    cor_ans_q1 = StringProperty('')
    cor_ans_q2 = StringProperty('')
    cor_ans_q3 = StringProperty('')
    cor_ans_q4 = StringProperty('')
    cor_ans_q5 = StringProperty('')

    t_f_cor_ans_q1 = StringProperty('')
    t_f_cor_ans_q2 = StringProperty('')
    t_f_cor_ans_q3 = StringProperty('')
    t_f_cor_ans_q4 = StringProperty('')
    t_f_cor_ans_q5 = StringProperty('')

    def load_data(self, file_path):
        """Загрузить данные из текстового файла в свойства класса."""
        questions_dict = {}
        with open(file_path, 'r') as file:
            lines = file.readlines()

        section = None
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.startswith('Audio:'):
                questions_dict['audio'] = line.split(':', 1)[1].strip().strip('"')
                continue

            if line == 'True/False Questions:':
                section = 't_f'
                continue

            if line == 'Fill in the Blanks Questions:':
                section = 'fill_in_the_blanks'
                continue

            if section == 't_f':
                if line.startswith('t_f_q'):
                    key, question = line.split(':', 1)
                    questions_dict[key.strip()] = question.strip().strip('"')
                elif line.startswith('t_f_ans_q'):
                    key, answer = line.split(':', 1)
                    questions_dict[key.strip()] = answer.strip().strip('"')

            if section == 'fill_in_the_blanks':
                if line.startswith('q'):
                    key, question = line.split(':', 1)
                    questions_dict[key.strip()] = question.strip().strip('"')
                elif line.startswith('q') and '_op' in line:
                    key, option = line.split(':', 1)
                    questions_dict[key.strip()] = option.strip().strip('"')
                elif line.startswith('cor_ans_q'):
                    key, answer = line.split(':', 1)
                    questions_dict[key.strip()] = answer.strip().strip('"')

        # Обновляем свойства класса данными из словаря
        for key, value in questions_dict.items():
            setattr(self, key, value)

    def update_screen_with_audio(self, file_name):
        """Обновить экран с вопросами на основе текущего аудиофайла."""
        text_file_path = os.path.join('assets/audio/questions', file_name + '.txt')
        self.load_data(text_file_path)

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
