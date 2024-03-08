from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import random
import json

APP_KV = """
<Libelle>:
    canvas:       
        Color:
            rgba: .1, 1, .1, .9
        Ellipse:
            group: 'libelle'
            size: 100, 100
            pos: (self.width-100)/2, (self.height-100)/2
"""

with open("synt_acc_data.json", "r") as file:
    data = json.loads(file.read())["data"]


#https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html mal ansehen

class Libelle(BoxLayout):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        print(data)

        self.pos_x = (self.width-100)/2
        self.pos_y = (self.height-100)/2
        Clock.schedule_interval(self.test_pos, 0.01)
        
    def test_pos(self, *args): 
        pos_x_target_test = [700, 1]
        pos_x_target = pos_x_target_test[0] if round(self.pos_x, 0) == round(pos_x_target_test[1], 0) else pos_x_target_test[1]
        self.pos_y = (self.height-100)/2  
        self.pos_x = (self.width-100)/2      
        # pos_x = self.get_pos_x(pos_x_target)
        pos_x = self.pos_x
        pos_y = self.pos_y
        self.canvas.get_group('libelle')[0].pos = pos_x, pos_y



    def __getCenterPoints():
        pass

    def get_pos_x(self, x, start_point = -1):
        pass

    def get_pos_y(self, y, start_point = -1):
        pass

    def get_pos_z(self, z, start_point = -1):
        pass


    def get_x_pos(self, pos_x_target):       
        self.pos_x = (self.width-100)/2 if self.pos_x < 1 else self.pos_x
        if round(self.pos_x, 0) == round(pos_x_target, 0):    
            print('equal') 
            return self.pos_x
        elif self.pos_x < pos_x_target: 
            print('to right')           
            # self.pos_x +=  (pos_x_target/self.pos_x)*2
            self.pos_x += 10
        elif self.pos_x > pos_x_target and self.pos_x > 0:    
            print('to left')   
            self.pos_x -= 10
            # self.pos_x -=  ((self.width-pos_x_target)/(self.width-self.pos_x))*2
        return self.pos_x


        # self.canvas.get_group('libelle')[0].pos = random.randrange(1, Window.width - 200), random.randrange(1, Window.height - 100)
        


class MainApp(App):
    def build(self):
        self.root = Builder.load_string(APP_KV)
        return Libelle()

if __name__ == '__main__':
    MainApp().run()