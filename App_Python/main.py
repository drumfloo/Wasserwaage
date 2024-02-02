from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import ScaleApp

class ScaleApp(App):
    def build(self):
        self.title = 'Multimedia App'
        return ScaleApp()

if __name__ == '__main__':
    ScaleApp().run()