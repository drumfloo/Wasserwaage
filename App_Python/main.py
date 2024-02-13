from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

from plyer import accelerometer
from kivy.uix.screenmanager import ScreenManager, Screen

class ConfigScreen(Screen):
        
    # def __init__(self, **kwargs):
    #     super(ConfigScreen, self).__init__(**kwargs)
    #     self.size_hint = (1, 1)
    
    def btn_back(self):
        print("BACK BUTTON...")
        sm = self.manager
        sm.current = 'start'
        

    def btn_go(self):
        print("GO...")
    
    def btn_checkConnection(self):
        print("CHECK_CONNECTION...")
        


class StartScreen(Screen):
   
    def btn_config(self):
        # go to configuration screen
        print("BTN_CONFIG...")
        sm = self.manager
        sm.current = 'config'



class ScaleApp(App):

    def build(self):
        
        Builder.load_file('StartScreen.kv')
        Builder.load_file('ConfigScreen.kv')
        sm = ScreenManager()
        start_screen = StartScreen(name='start')
        config_screen = ConfigScreen(name='config')
        sm.add_widget(start_screen)
        sm.add_widget(config_screen)
        return sm



    def get_acceleration(self):
        accelerometer.enable()
        acceleration = accelerometer.acceleration
        self.label.text = f"Neigung: {acceleration}"
        print(acceleration)



if __name__ == '__main__':
    ScaleApp().run()
