from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class ScaleGridLayout(GridLayout):
    pass

class ConfigGridLayout(GridLayout):
    pass



class ScaleApp(App):
    def build(self):
        self.title = 'Scale-App'
        return ScaleApp()

if __name__ == '__main__':
    ScaleApp().run()