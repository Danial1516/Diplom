from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.utils import get_color_from_hex
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from datetime import datetime, timedelta
from kivy.metrics import dp  # Не забудьте импортировать dp

class CalendarScreen(MDScreen):
    best_streak = StringProperty("0")
    current_streak = StringProperty("0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.visited_days = set()

    def update_calendar(self):
        # Обновить календарь и серию дней
        self.ids.calendar_layout.clear_widgets()
        today = datetime.today().date()
        # Пример: последние 30 дней, включая сегодня
        days = [today - timedelta(days=i) for i in range(30)]
        days.reverse()
        current_streak = 0
        best_streak = 0
        temp_streak = 0
        for day in days:
            day_label = MDLabel(
                text=str(day.day),
                halign="center",
                theme_text_color="Primary",
                size_hint=(None, None),
                size=(dp(40), dp(40)),
            )
            if day in self.visited_days:
                day_label.md_bg_color = get_color_from_hex("#005794D9")
                temp_streak += 1
                current_streak = temp_streak
                if temp_streak > best_streak:
                    best_streak = temp_streak
            else:
                temp_streak = 0
            self.ids.calendar_layout.add_widget(day_label)
        self.best_streak = str(best_streak)
        self.current_streak = str(current_streak)

    def mark_visited(self, visit_date):
        # Отметить день посещенным
        self.visited_days.add(visit_date)
        self.update_calendar()
