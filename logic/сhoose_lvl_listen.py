from kivymd.uix.screen import MDScreen

class ChooseLvlListenScreen(MDScreen):
    def set_level(self, level):
        """Установите уровень и перейдите на экран ListenScreen."""
        # Установите уровень в ListenScreen
        listen_screen = self.manager.get_screen('listen_screen')
        listen_screen.set_level(level)

        # Переход на экран ListenScreen
        self.manager.current = 'listen_screen'
