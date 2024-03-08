from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from mqtt.mqtt_connector import MQTTconnector
from kivy.clock import Clock
from kivy.properties import NumericProperty,BooleanProperty



class ConfigScreen(Screen):
        
    credentialKeys = ["mqtt_host", "port", "userName", "password", "fullTopic", "intervals", "dimensions"]
    userIN = {}

    def __init__(self, **kwargs):
         super(ConfigScreen, self).__init__(**kwargs)
         self.size_hint = (1, 1)
         #self.mq = MQTTconnector()       

    def on_pre_enter(self, *args):
        self.fill_fields()

    def fill_fields(self, config_path = "mqtt/mqtt_config.json"):
        print("fill")
        with open(config_path, "r") as file:
            dict_config = json.load(file)
        
        self.ids.mqtt_host_input.text = dict_config["host"]
        self.ids.port_input.text = dict_config["port"]
        self.ids.full_topic_input.text = dict_config["topic"]
        self.ids.username_input.text = dict_config["username"]
        self.ids.password_input.text = dict_config["password"]
        


    def login_data_fetcher(self, type, value):
        """Fetches login data for mqtt connection. Saved as 
        key:value pairs in a Python dict"""
        self.userIN[type] = value
        
        


    # Buttons
    def btn_back(self):
        """Navigate back to *sm.current* value defined in ScaleApp class"""
        sm = self.manager
        sm.current = 'start'     
        

    def btn_go(self):
        """Checks necessary login credentials"""
        for value in self.credentialKeys:
            if value not in self.userIN:
                self.notification("Error - connection not set through missing informations")
            
        sm = self.manager
        sm.current = 'start'


    
    def btn_checkConnection(self):
        """Checks if connection credentials set correct and connection can be ethablished"""
        try:
            self.mq = MQTTconnector(host=self.userIN['mqtt_host'],port=int(self.userIN['port']),topic=self.userIN['fullTopic'])
            self.mq.build_connection()
            
            self.save_config()
            self.notification("Connected")

        except Exception as e:
            print(type(str(e)))
            self.notification(str(e) + " Connection not ready")


    def save_config(self):
        with open("mqtt/mqtt_config.json", "r") as file:
            dict_config = json.load(file)

        dict_config["host"] = self.userIN["mqtt_host"]
        dict_config["port"] = self.userIN["port"]
        dict_config["topic"] = self.userIN["fullTopic"]
        dict_config["username"] = self.userIN["userName"]
        dict_config["password"] = self.userIN["password"]

        with open("mqtt/mqtt_config.json", "w") as outfile: 
            json.dump(dict_config, outfile)
    
    # Notification
    def notification(self, msg: str):
        """Notification function to show popup. *msg* means the message to show in the popup"""
        popup = Popup(
        title = msg,
        #content='Cant establish a working connection...',
        size_hint = (None, None),
        size = (250, 100), #size=(Window.width / 3, Window.height / 3),
        auto_dismiss = True,
        )
        # on_press=popup.dismiss
        popup.open()
        


class StartScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.xval = NumericProperty(0.0)
        self.direction = BooleanProperty(False)

    
    def btn_config(self):
        """Switches to configuration panel"""
        sm = self.manager
        sm.current = 'config'
    
    

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    #     self.pos_x = (self.width-100)/2
    #     self.pos_y = (self.height-100)/2
    #     Clock.schedule_interval(self.test_pos, 0.01)
        
    # def test_pos(self, *args): 
    #     pos_x_target_test = [700, 1]
    #     pos_x_target = pos_x_target_test[0] if round(self.pos_x, 0) == round(pos_x_target_test[1], 0) else pos_x_target_test[1]
    #     self.pos_y = (self.height-100)/2        
    #     pos_x = self.get_x_pos(pos_x_target)
    #     pos_y = self.pos_y

    #     print(self.canvas)

    #     self.canvas.get_group('libelle')[0].pos = pos_x, pos_y


    # def get_x_pos(self, pos_x_target):       
    #     self.pos_x = (self.width-100)/2 if self.pos_x < 1 else self.pos_x
    #     if round(self.pos_x, 0) == round(pos_x_target, 0):    
    #         print('equal') 
    #         return self.pos_x
    #     elif self.pos_x < pos_x_target: 
    #         print('to right')           
    #         # self.pos_x +=  (pos_x_target/self.pos_x)*2
    #         self.pos_x += 10
    #     elif self.pos_x > pos_x_target and self.pos_x > 0:    
    #         print('to left')   
    #         self.pos_x -= 10
    #         # self.pos_x -=  ((self.width-pos_x_target)/(self.width-self.pos_x))*2
    #     return self.pos_x

    

class Libelle(Screen):
    xval = NumericProperty(0.0)
    direction = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(Libelle, self).__init__(**kwargs)
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
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#         self.pos_x = (self.width-100)/2
#         self.pos_y = (self.height-100)/2
#         Clock.schedule_interval(self.test_pos, 0.01)
        
#     def test_pos(self, *args): 
#         pos_x_target_test = [700, 1]
#         pos_x_target = pos_x_target_test[0] if round(self.pos_x, 0) == round(pos_x_target_test[1], 0) else pos_x_target_test[1]
#         self.pos_y = (self.height-100)/2        
#         pos_x = self.get_x_pos(pos_x_target)
#         pos_y = self.pos_y

#         print(self.canvas)

#         self.canvas.get_group('libelle')[0].pos = pos_x, pos_y


#     def get_x_pos(self, pos_x_target):       
#         self.pos_x = (self.width-100)/2 if self.pos_x < 1 else self.pos_x
#         if round(self.pos_x, 0) == round(pos_x_target, 0):    
#             print('equal') 
#             return self.pos_x
#         elif self.pos_x < pos_x_target: 
#             print('to right')           
#             # self.pos_x +=  (pos_x_target/self.pos_x)*2
#             self.pos_x += 10
#         elif self.pos_x > pos_x_target and self.pos_x > 0:    
#             print('to left')   
#             self.pos_x -= 10
#             # self.pos_x -=  ((self.width-pos_x_target)/(self.width-self.pos_x))*2
#         return self.pos_x


        #self.canvas.get_group('libelle')[0].pos = random.randrange(1, Window.width - 200), random.randrange(1, Window.height - 100)
        

class ScaleApp(App):
    
    def build(self):        
        Builder.load_file('StartScreen.kv')
        Builder.load_file('ConfigScreen.kv')
        sm = ScreenManager()
        start_screen = StartScreen(name='start')
        config_screen = ConfigScreen(name='config')
        libelle = Libelle()

        sm.add_widget(start_screen)
        sm.add_widget(config_screen)
        sm.add_widget(libelle)
        return sm

    


if __name__ == '__main__':
    ScaleApp().run()
    mq = MQTTconnector()
    mq.build_connection()
    mq.send_msg("Sende eine Nachricht")





