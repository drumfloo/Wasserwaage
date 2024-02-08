from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from plyer import accelerometer

class StartScreen(Screen):
    #Builder.load_file('StartScreen.kv')
    pass

class ConfigScreen(Screen):
    #Builder.load_file('ConfigScreen.kv')
    pass
    def check_connection(self):
        print("Checking connection...")

    def go(self):
        print("Going to the next page...")

    def back(self):
        print("Going back...")

class ScaleApp(App):
    def build(self):
        self.title = 'Scale-App'        
        #Builder.load_string(open('ConfigScreen.kv', encoding='utf-8').read())
        #Builder.load_string(open('StartScreen.kv', encoding='utf-8').read())       
        Builder.load_file('ConfigScreen.kv')
        Builder.load_file('StartScreen.kv')
        sm = ScreenManager()
        start_screen = StartScreen(name='start')
        config_screen = ConfigScreen(name='config')
        sm.add_widget(start_screen)
        sm.add_widget(config_screen)
        return sm 

    # def get_acceleration(self):
    #     accelerometer.enable()
    #     acceleration = accelerometer.acceleration
    #     print(acceleration)

if __name__ == '__main__':
    ScaleApp().run()









# ERSTE FASSUNG CONFIG_SCREEN

# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.lang.builder import Builder

# from plyer import accelerometer
# from kivy.uix.screenmanager import ScreenManager, Screen

# class Config_page(BoxLayout):
#     Builder.load_file('Config_page.kv')
    
#     # def __init__(self, **kwargs):
#     #     super(Config_page, self).__init__(**kwargs)
#     #     self.size_hint = (1, 1)

# class Scale_page(BoxLayout):
#     pass



# class ScaleApp(App):
#     def build(self):
#         self.title = 'Scale-App'
#         #self.get_acceleration()
#         return Config_page()
    
#     def get_acceleration(self):
#         accelerometer.enable()
#         acceleration = accelerometer.acceleration
#         #self.label.text = f"Neigung: {acceleration}"
#         print(acceleration)



# if __name__ == '__main__':
#     ScaleApp().run()
