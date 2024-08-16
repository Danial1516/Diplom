from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivymd.uix.widget import MDWidget
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    CommonElevationBehavior,
)


class ElevatedWidget(
    CommonElevationBehavior,
    RectangularRippleBehavior,
    ButtonBehavior,
    MDWidget,
):
    _elev = 0  # previous elevation value

    def on_press(self, *args):
        if not self._elev:
            self._elev = self.elevation
        Animation(elevation=self.elevation + 2, d=0.4).start(self)

    def on_release(self, *args):
        Animation.cancel_all(self, "elevation")
        Animation(elevation=self._elev, d=0.1).start(self)