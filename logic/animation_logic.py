# Diplom/logic/animation_logic.py

from kivy.animation import Animation
from kivy.uix.image import Image

def animate_login_screen(screen):
    # Анимация размытия фона
    blur_animation = Animation(size=(screen.width, screen.height), duration=2)

    # Анимация появления текста
    label_animation = Animation(opacity=1, duration=2)

    # Применение анимации к виджетам
    screen.ids.login_label.opacity = 0
    screen.ids.login_email.opacity = 0
    screen.ids.login_password.opacity = 0
    screen.ids.login_button.opacity = 0
    screen.ids.register_label.opacity = 0

    blur_animation.start(screen.ids.login_image)
    label_animation.start(screen.ids.login_label)
    label_animation.start(screen.ids.login_email)
    label_animation.start(screen.ids.login_password)
    label_animation.start(screen.ids.login_button)
    label_animation.start(screen.ids.register_label)
