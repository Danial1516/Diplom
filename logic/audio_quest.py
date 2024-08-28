import os

from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, DictProperty, BooleanProperty

class AudioQuestionsScreen(MDScreen):
    selected_option = StringProperty('')
    selected_options = DictProperty({})
    is_checked = BooleanProperty(False)

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

    def on_pre_enter(self, *args):
        """Сбросить экран при каждом входе на него."""
        self.reset_screen()
        self.is_checked = False

    def reset_screen(self):
        """Сбросить все ответы и цвета к исходному состоянию."""
        self.selected_option = ''
        self.selected_options.clear()

        # Сбросить цвет всех кнопок True/False
        for i in range(1, 6):
            true_option_id = f'true_option_{i}'
            false_option_id = f'false_option_{i}'
            if true_option_id in self.ids:
                self.ids[true_option_id].md_bg_color = [255 / 255, 255 / 255, 255 / 255, 1]  # Белый цвет
            if false_option_id in self.ids:
                self.ids[false_option_id].md_bg_color = [255 / 255, 255 / 255, 255 / 255, 1]  # Белый цвет

        # Сбросить цвет всех кнопок Fill in the Blanks
        for i in range(1, 6):
            for j in range(1, 4):
                option_id = f'option_{j}_q{i}'
                if option_id in self.ids:
                    self.ids[option_id].md_bg_color = [255 / 255, 255 / 255, 255 / 255, 1]  # Белый цвет

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
        if self.is_checked:
            return

        # Сбрасываем цвета обеих кнопок к исходному белому
        self.ids[f'true_option_{question_id}'].md_bg_color = [255 / 255, 255 / 255, 255 / 255, 1]
        self.ids[f'false_option_{question_id}'].md_bg_color = [255 / 255, 255 / 255, 255 / 255, 1]

        # Подсвечиваем выбранный пользователем вариант
        selected_id = f'{option}_option_{question_id}'
        self.ids[selected_id].md_bg_color = [173 / 255, 216 / 255, 230 / 255, 1]

        # Сохраняем выбранный вариант в словарь selected_options
        self.selected_options[f't_f_q{question_id}'] = selected_id

        # Сохраняем выбранный вариант для дальнейшей проверки
        self.selected_option = option

    def select_fill_in_the_blanks_option(self, option_id):
        if self.is_checked:
            return

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

    def check_answers(self):
        self.is_checked = True
        # Проверка True/False вопросов
        for i in range(1, 6):
            # Получаем выбранный пользователем ответ (ID кнопки)
            user_answer_id = self.selected_options.get(f't_f_q{i}', '')
            # Получаем правильный ответ из атрибута (например, 'True' или 'False')
            correct_answer = getattr(self, f't_f_ans_q{i}').replace('"', '')  # Убираем кавычки

            # Определяем ID для вариантов ответа
            true_option_id = f'true_option_{i}'
            false_option_id = f'false_option_{i}'

            # Определяем ID правильного ответа в зависимости от значения correct_answer
            correct_option_id = true_option_id if correct_answer.lower() == 'true' else false_option_id

            # Проверяем, выбрал ли пользователь какой-либо вариант ответа
            if user_answer_id:
                # Если выбран правильный вариант
                if user_answer_id == correct_option_id:
                    # Красим правильный вариант в зелёный
                    self.ids[user_answer_id].md_bg_color = [0 / 255, 128 / 255, 0 / 255, 1]
                else:
                    # Если выбран неправильный вариант
                    self.ids[user_answer_id].md_bg_color = [255 / 255, 0 / 255, 0 / 255,
                                                            1]  # Красим неверный ответ в красный
                    self.ids[correct_option_id].md_bg_color = [0 / 255, 128 / 255, 0 / 255,
                                                               1]  # Красим правильный ответ в зелёный
            else:
                # Если вариант не выбран пользователем, подсвечиваем правильный ответ зеленым
                self.ids[correct_option_id].md_bg_color = [0 / 255, 128 / 255, 0 / 255, 1]  # Зеленый цвет

        # Проверка Fill in the Blanks вопросов
        for i in range(1, 6):
            user_answer_id = self.selected_options.get(f'q{i}', '')
            correct_answer = getattr(self, f'cor_ans_q{i}')

            if user_answer_id:
                # Получаем текст из MDLabel внутри MDCard
                user_answer_text = self.ids[user_answer_id].children[0].text

                if user_answer_text == correct_answer:
                    self.ids[user_answer_id].md_bg_color = [0 / 255, 128 / 255, 0 / 255, 1]  # Зеленый цвет
                else:
                    self.ids[user_answer_id].md_bg_color = [255 / 255, 0 / 255, 0 / 255, 1]  # Красный цвет
                    # Находим правильный ответ среди ID и меняем его цвет на зеленый
                    for option_id in ['option_1_q' + str(i), 'option_2_q' + str(i), 'option_3_q' + str(i)]:
                        if self.ids[option_id].children[0].text == correct_answer:
                            self.ids[option_id].md_bg_color = [0 / 255, 128 / 255, 0 / 255, 1]  # Зеленый цвет
                            break
            else:
                # Если вариант не выбран пользователем, подсвечиваем правильный ответ зеленым
                for option_id in [f'option_1_q{i}', f'option_2_q{i}', f'option_3_q{i}']:
                    if self.ids[option_id].children[0].text == correct_answer:
                        self.ids[option_id].md_bg_color = [0 / 255, 128 / 255, 0 / 255, 1]  # Зеленый цвет
                        break