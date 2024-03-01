from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
import random

Builder.load_string('''
<LineCircle1>:
    canvas:
        Color:
            rgba: .1, 1, .1, .9
        Line:
            width: 2
            circle:
                (self.pos_x, self.pos_y, min(50, 50)/2)
''')

class LineCircle1(Widget):
    pos_x = 50
    pos_y = 50

class LineExtendedApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.win_width, self.win_height = Window.size
        self.circle_radius = 50

    def build(self):
        libelle = LineCircle1()
        self.libelle = libelle
        Clock.schedule_interval(self.update, 1./60.)
        return libelle

    def update(self, dt):
        # Get new random position for the circle within the window bounds
        self.libelle.pos = (random.randint(self.circle_radius, self.win_width - self.circle_radius),
                           random.randint(self.circle_radius, self.win_height - self.circle_radius))

if __name__ == '__main__':
    LineExtendedApp().run()