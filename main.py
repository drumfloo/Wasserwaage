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
from plyer import accelerometer, facades
import time



class ConfigScreen(Screen):
        
    credentialKeys = ["mqtt_host", "port", "userName", "password", "fullTopic", "intervals", "dimensions"]
    userIN = {}

    def __init__(self, **kwargs):
         super(ConfigScreen, self).__init__(**kwargs)
         self.size_hint = (1, 1)
         #self.mq = MQTTconnector()       

    def on_pre_enter(self, *args):
        time.sleep(1)
        self.fill_fields()

    def fill_fields(self, config_path = "mqtt/mqtt_config.json"):
        try:
            print("fill")
            with open(config_path, "r") as file:
                dict_config = json.load(file)
            
            self.ids.mqtt_host_input.text = dict_config["host"]
            self.ids.port_input.text = dict_config["port"]
            self.ids.full_topic_input.text = dict_config["topic"]
            self.ids.username_input.text = dict_config["username"]
            self.ids.password_input.text = dict_config["password"]
        except Exception as e:
            print(e)
        


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


    
    def btn_check_connection(self):
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
    pos_y = NumericProperty(0.5)
    pos_x = NumericProperty(0.5)
    pos_z = NumericProperty(0.5)

    def __init__(self, **kw):
        super().__init__(**kw)
        # self.direction = BooleanProperty(False)
        try:
            accelerometer.enable()
            Clock.schedule_interval(self.get_acceleration, 1 / 60.)  
        except Exception as e:
            print(e)
              
      

        #self.movement()

    
    def btn_config(self):
        """Switches to configuration panel"""
        sm = self.manager
        sm.current = 'config'


    def update_dragonfly(self, pos):
        x = round(pos[0], 1)
        y = round(pos[1], 1)
        self.pos_x = x / 20 + 0.5
        self.pos_y = y / 20 + 0.5

        #Original
        # self.pos_x = pos[0] / 20 + 0.5
        # self.pos_y = pos[1] / 20 + 0.5


    def get_acceleration(self, dt):
        try:
            val = accelerometer.acceleration[:3]
            print("VAL:")
            print(val)
            print(type(val))

            if not val == (None, None, None):            
                #self.ids.x_label.text = "X: " + str(val[0])
                self.ids.x_label.text = f"X: {val[0]:.3f}"  #Test
                print(str(val[0]))

                #self.ids.y_label.text = "Y: " + str(val[1])
                self.ids.y_label.text = f"Y: {val[1]:.3f}"  #Test
                print(str(val[1]))

                #self.ids.z_label.text = "Z: " + str(val[2])
                self.ids.z_label.text = f"Z: {val[2]:.3f}"  #Test
                print(str(val[2]))

                self.update_dragonfly(val)
        except Exception as e:
            print(e) 

  

class ScaleApp(App):   
    def build(self):
        facades.Orientation.set_sensor('landscape')        
        Builder.load_file('StartScreen.kv')
        Builder.load_file('ConfigScreen.kv')
        sm = ScreenManager()
        
        start_screen = StartScreen(name='start')
        config_screen = ConfigScreen(name='config')

        sm.add_widget(start_screen)
        sm.add_widget(config_screen)
        return sm
    
if __name__ == '__main__':
    ScaleApp().run()
    mq = MQTTconnector()
    mq.build_connection()
    mq.send_msg("Sende eine Nachricht")

#facades.Orientation.set_landscape(reverse=False)
# facades.Orientation.set_sensor('landscape')