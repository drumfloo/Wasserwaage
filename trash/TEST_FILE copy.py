from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.core.window import Window
import random

Builder.load_string('''
<GridLayout1>:
    <LineCircle1>:
        group: 'libelle'
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


class GridLayout1(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class LineExtendedApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.win_width, self.win_height = Window.size
        self.circle_radius = 50


    def build(self):
        # create the grid layout as before
        self.root = GridLayout1(cols=2, padding=50, spacing=50)
        self.libelle = LineCircle1()
        self.root.add_widget(self.libelle)

        # schedule the update method at regular intervals
        # Clock.schedule_interval(self.update, 1./60.)
        Clock.schedule_interval(self.update, 0.5)

        return self.root

    def update(self, dt):
        
        # get new random position for the circle within the window bounds
        #self.libelle = LineCircle1()
        print(self.root.canvas.get_group('libelle'))
        self.root.canvas.get_group('libelle')[0].pos = (0,0)

        # self.libelle.pos = (random.randint(self.circle_radius, self.win_width - self.circle_radius),
                    #    random.randint(self.circle_radius, self.win_height - self.circle_radius))
        root = self.root      
        print(dt)
        print(self.libelle.pos)
        root.remove_widget(self.libelle)
        
        root.add_widget(self.libelle)


    # def update(self, dt):
    #     # Get new random position for the circle within the window bounds
    #     libelle = self.libelle = LineCircle1()
    #     libelle.pos = (random.randint(self.circle_radius, self.win_width - self.circle_radius),
    #                 random.randint(self.circle_radius, self.win_height - self.circle_radius))
    #     root = self.root
    #     root.remove_widget(self.libelle)
    #     root.add_widget(libelle)

if __name__ == '__main__':
    LineExtendedApp().run()