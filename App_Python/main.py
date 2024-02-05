from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

from plyer import accelerometer

class config_page(BoxLayout):
    Builder.load_file('config_page.kv')
    
    # def __init__(self, **kwargs):
    #     super(config_page, self).__init__(**kwargs)
    #     self.size_hint = (1, 1)




class ScaleApp(App):
    def build(self):
        self.title = 'Scale-App'
        #self.get_acceleration()
        return config_page()
    
    def get_acceleration(self):
        accelerometer.enable()
        acceleration = accelerometer.acceleration
        #self.label.text = f"Neigung: {acceleration}"
        print(acceleration)






if __name__ == '__main__':
    ScaleApp().run()