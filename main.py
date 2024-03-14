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
from configparser import ConfigParser
from kivy.clock import Clock
from plyer import accelerometer, orientation
import time
import ssl
from kivy.config import Config

Config.set('graphics', 'orientation', 'landscape')



class ConfigScreen(Screen):
        
    userIN = {}

    def __init__(self, **kwargs):
         super(ConfigScreen, self).__init__(**kwargs)
         self.size_hint = (1, 1)
         self.mq = MQTTconnector()       

    def on_pre_enter(self, *args):
        time.sleep(0.5)
        self.load_saved_values()


    def save_values(self):
        config = ConfigParser()
        
        try:
            config.read('config.ini')
        except FileNotFoundError:
            pass
        
        config['Credentials'] = {
            "host": self.userIN["mqtt_host"],
            "port": self.userIN["port"],
            "topic": self.userIN["fullTopic"],
            "username": self.userIN["userName"],
            "password": self.userIN["password"]
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)



    def load_saved_values(self):
        config = ConfigParser()

        
        try:
            config.read('config.ini')
        except FileNotFoundError:
            return

        if 'Credentials' in config:
            credentials = config['Credentials']
            if 'username' in credentials:
                self.ids.username_input.text = credentials['username']
            if 'password' in credentials:
                self.ids.password_input.text = credentials['password']
            if 'host' in credentials:
                self.ids.mqtt_host_input.text   = credentials['host']
            if 'port' in credentials:
                self.ids.port_input.text = credentials['port']               
            if 'topic' in credentials:             
                self.ids.full_topic_input.text = credentials["topic"]
        
        


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
        for value in ["mqtt_host", "port", "fullTopic"]:
            if self.userIN[value] == "":
                self.notification("Error - connection not set through missing informations")
            
        sm = self.manager
        sm.current = 'start'


    
    def btn_check_connection(self):
        """Checks if connection credentials set correct and connection can be ethablished"""
        try:
            self.mq = MQTTconnector(shost=self.userIN['mqtt_host'],sport=int(self.userIN['port']),stopic=self.userIN['fullTopic'])
            self.mq.build_connection()
            
            self.save_values()
            self.notification("Connected")

        except Exception as e:
            print(e)
            self.notification(str(e) + " Connection not ready")

    
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


    arr_of_X = [0, 0]
    arr_of_Y = [0, 0]


    def __init__(self, **kw):
        super().__init__(**kw)
        # self.direction = BooleanProperty(False)
        try:
            accelerometer.enable()
            Clock.schedule_interval(self.get_acceleration, 1 / 60.)
            self.mq = MQTTconnector()  
        except Exception as e:
            print(e)
              


    
    def btn_config(self):
        """Switches to configuration panel"""
        sm = self.manager
        sm.current = 'config'



    # Libellen-smoother*********************************************   
    def collector_X_Y(self, pos):
        """Takes the sensor data Tuple and adds to x/y array respectively"""
        if len(self.arr_of_X) < 6 and len(self.arr_of_Y) < 6:
            self.arr_of_X.append(-1*pos[1])
            self.arr_of_Y.append(pos[0])
        else:
            print(f"collector_X_Y() else-clause = X:{self.arr_of_X} Y:{self.arr_of_Y}")
            self.average_pos(self.arr_of_X, self.arr_of_Y)
            
            
    def average_pos(self, arrayX, arrayY):
        """Gets acceleration data, sends it to label & to the smoothening-process logic"""
        self.pos_x = (round(sum(arrayX) / len(arrayX), 1)) / 20 + 0.5
        self.pos_y = (round(sum(arrayY) / len(arrayY), 1)) / 20 + 0.5

        self.arr_of_X = [0, 0]
        self.arr_of_Y = [0, 0]


    def get_acceleration(self, dt):
        try:
            val = accelerometer.acceleration[:3]
            
            if not val == (None, None, None):            
                self.ids.x_label.text = "X: " + str(val[0])
                self.ids.y_label.text = "Y: " + str(val[1])
                self.ids.z_label.text = "Z: " + str(val[2])
                self.collector_X_Y(val)
                self.mq.send_msg(str(val))
        except Exception as e:
            print(e) 

  

class ScaleApp(App):   
    def build(self):        
        Builder.load_file('StartScreen.kv')
        Builder.load_file('ConfigScreen.kv')
        sm = ScreenManager()
        start_screen = StartScreen(name='start')
        config_screen = ConfigScreen(name='config')
        orientation.set_landscape()
        ssl._create_default_https_context = ssl._create_stdlib_context
        sm.add_widget(start_screen)
        sm.add_widget(config_screen)
        
        return sm
    
if __name__ == '__main__':
    ScaleApp().run()
