from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.properties import NumericProperty,BooleanProperty
from kivy.clock import Clock

class MyWidget(BoxLayout):
    xval = NumericProperty(0.0)
    direction = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_value, 0.016)
    def update_value(self, dt):
        if(self.direction==False):
            self.xval += 0.01
            if(self.xval>=1.0):
                print("Test")
                self.direction=True
        else:
            self.xval -= 0.01
            if(self.xval<=0.0):
                self.direction=False
    pass
class MyApp(App):
    def build(self):
        Builder.load_file("test.kv")
        
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()