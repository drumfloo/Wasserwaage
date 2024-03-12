from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from mqtt.mqtt_connector import MQTTconnector
from kivy.clock import Clock
from kivy.properties import NumericProperty,BooleanProperty
import json 
from kivy.uix.boxlayout import BoxLayout

from kivy.clock import Clock
from plyer import accelerometer
import time



# with open("synt_acc_data.json", "r") as file:
#     test_data = json.loads(file.read())['data']


# class AccelerometerTest(BoxLayout):
#     def __init__(self):
#         super().__init__()
#         self.sensorEnabled = False


#     def get_acceleration(self, dt):
#         val = accelerometer.acceleration[:3]
#         if not val == (None, None, None):
#             self.ids.x_label.text = "X: " + str(val[0])
#             self.ids.y_label.text = "Y: " + str(val[1])
#             self.ids.z_label.text = "Z: " + str(val[2])


# class AccelerometerTestApp(App):
#     def build(self):
#         return AccelerometerTest()

#     def on_pause(self):
#         return True



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
        

class Libelle(Screen):
    xval = NumericProperty(0.0)
    yval = NumericProperty(0.0)
    direction = BooleanProperty(False)
    test = BooleanProperty(True)
    #start_screen = StartScreen()
    
    
    
    def __init__(self, **kwargs):
        
        super(Libelle, self).__init__(**kwargs)
        #Clock.schedule_interval(self.update_value, 0.016)
    

        
    def update_value(self, dt):
        print(self.yval)
        print((float(dt[1]) - float(self.yval)) / 10)
        self.yval += (float(dt[1]) - float(self.yval)) / 10
        print(dt[0])
        self.xval += (float(dt[0]) - float(self.xval)) / 10
        print(self.xval)
        print((float(dt[0]) - float(self.yval)) / 10)
        print()
        #if self.test:
         #   self.run_test()
          #  return             

        
    def run_test(self):
        if(self.direction==False):
            self.xval += 0.01
            if(self.xval>=1.0):
                print("Test")
                self.direction=True
        else:
            self.xval -= 0.01
            if(self.xval<=0.0):
                self.direction=False

class StartScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.xval = NumericProperty(0.0)
        self.direction = BooleanProperty(False)
        accelerometer.enable()
        Clock.schedule_interval(self.get_acceleration, 1 / 20.)
        self.libelle = Libelle()
        #self.movement()

    
    def btn_config(self):
        """Switches to configuration panel"""
        sm = self.manager
        sm.current = 'config'

    
    # def get_test_data(self):
    #     with open("synt_acc_data.json", "r") as file:
    #         test_data = json.loads(file.read())['data']
    #         return test_data

    def get_acceleration(self, dt):
        try:
            val = accelerometer.acceleration[:3]
            print("VAL:")
            print(val)
            print(type(val))
        

        
            if not val == (None, None, None):            
                self.ids.x_label.text = "X: " + str(val[0])
                print(str(val[0]))
                self.ids.y_label.text = "Y: " + str(val[1])
                print(str(val[1]))
                self.ids.z_label.text = "Z: " + str(val[2])
                print(str(val[2]))
                print()
                self.libelle.update_value(val)
        except Exception as e:
            print(e) 

    

    # def get_X(self):
    #     data = self.get_test_data()
    #     for i in data:
    #         return str(i[0])

    # def get_Y(self):
    #     data = self.get_test_data()
    #     for i in data:
    #         return str(i[1])

    # def get_Z(self):
    #     data = self.get_test_data()
    #     for i in data:
    #         return str(i[2])
    
   
   
    # def send_data(self, axe):
    #     data = self.get_test_data()
    #     for i in data:
    #         if axe == "x":
    #             print(str(i[0])) #DEBUG
    #             return str(i[0])
    #         elif axe == "y":
    #             print(str(i[1]))#DEBUG
    #             return str(i[1])
    #         else: 
    #             print(str(i[2]))#DEBUG
    #             return str(i[2])





     
 
    
    # def get_test_data(self):
    #     with open("synt_acc_data.json", "r") as file:
    #         test_data = json.loads(file.read())['data']
    #         return test_data


    # def movement(self):
    #     print("movement() ausgeführt")
    #     data = self.get_test_data()
    #     self.ids.Label_X = "ÜBERSCHRIEBEN"

        #for i in data:            
            # self.ids.Label_X.text = str(i[0])
            # self.ids.Label_Y.text = str(i[1])
            # self.ids.Label_Z.text = str(i[2])

            # self.label_x.text = f"X: {self.xval:.2f}"  
            # self.label_y.text = f"Y: {self.xval:.2f}"  
            # self.label_z.text = f"Z: {self.xval:.2f}"  
  

class ScaleApp(App):   
    def build(self):        
        Builder.load_file('StartScreen.kv')
        Builder.load_file('ConfigScreen.kv')
        sm = ScreenManager()
        start_screen = StartScreen(name='start')
        config_screen = ConfigScreen(name='config')
        #libelle = Libelle()

        sm.add_widget(start_screen)
        sm.add_widget(config_screen)
        #sm.add_widget(libelle)
        return sm
    
if __name__ == '__main__':
    ScaleApp().run()
    mq = MQTTconnector()
    mq.build_connection()
    mq.send_msg("Sende eine Nachricht")
