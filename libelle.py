from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import random

APP_KV = """
<CanvasTest>:
    canvas:       
        Color:
            rgba: .1, 1, .1, .9
        Ellipse:
            group: 'libelle'
            size: 100, 100
            pos: (self.width-100)/2, (self.height-100)/2
"""

class CanvasTest(BoxLayout):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_interval(self.test_pos, 1)
        
    def test_pos(self, *args):
        print(self.height)

        x_pos = (self.width-100)/2
        y_pos = (self.height-100)/2
        self.canvas.get_group('libelle')[0].pos = x_pos, y_pos


        # self.canvas.get_group('libelle')[0].pos = random.randrange(1, Window.width - 200), random.randrange(1, Window.height - 100)
        


class MainApp(App):
    def build(self):
        self.root = Builder.load_string(APP_KV)
        return CanvasTest()

if __name__ == '__main__':
    MainApp().run()