from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder



class config_page(BoxLayout):
    Builder.load_file('config_page.kv')
    def test(self):
        pass

# class ConfigGridLayout(GridLayout):
#     pass



class ScaleApp(App):
    def build(self):
        self.title = 'Scale-App'
        return config_page()

if __name__ == '__main__':
    ScaleApp().run()


# ['lr-tb', 'tb-lr', 'rl-tb', 'tb-rl', 'lr-bt', 'bt-lr', 'rl-bt', 'bt-rl']
