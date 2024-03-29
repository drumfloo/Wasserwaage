from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from mqtt.mqtt_connector import MQTTconnector
from kivy.clock import Clock
from kivy.properties import NumericProperty,BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from configparser import ConfigParser
from kivy.clock import Clock
from plyer import accelerometer, orientation
import time, ssl
from kivy.config import Config

Config.set('graphics', 'orientation', 'landscape')


class ConfigScreen(Screen):
        
    userIN = {}

    def __init__(self, **kwargs):
         super(ConfigScreen, self).__init__(**kwargs)
         self.size_hint = (1, 1)
         self.mq = MQTTconnector()       

    def on_pre_enter(self, *args):
        '''Author Necip After enter fill text fields'''
        time.sleep(0.5)
        self.load_saved_values()


    def save_values(self):
        '''Author Necip Save the user input in a Config file'''
        config = ConfigParser()
        
        try:
            config.read('config.ini')
        except FileNotFoundError:
            pass

        if "userName" in self.userIN:
            pass
        else:
            self.userIN["userName"] = ""

        if "password" in self.userIN:
            pass
        else:
            self.userIN["password"] = ""
        
        config['Credentials'] = {
            "host": self.userIN.get("mqtt_host"),
            "port": self.userIN.get("port"),
            "topic": self.userIN.get("fullTopic"),
            "username": self.userIN.get("userName"),
            "password": self.userIN.get("password")
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)



    def load_saved_values(self):
        '''Author Necip Read Config file'''
        config = ConfigParser()

        
        try:
            config.read('config.ini')
        except FileNotFoundError:
            return

        if 'Credentials' in config:
            credentials = config['Credentials']
            if 'username' in credentials:
                self.ids.username_input.text = credentials.get('username')
            if 'password' in credentials:
                self.ids.password_input.text = credentials.get('password')
            if 'host' in credentials:
                self.ids.mqtt_host_input.text   = credentials.get('host')
            if 'port' in credentials:
                self.ids.port_input.text = credentials.get('port')               
            if 'topic' in credentials:             
                self.ids.full_topic_input.text = credentials.get("topic")
        
        


    def login_data_fetcher(self, type, value):
        """Author Florian Fetches login data for mqtt connection. Saved as 
        key:value pairs in a Python dict"""
        self.userIN[type] = value
        
        


# Buttons *************************************************  
    def btn_back(self):
        """Navigate back to *sm.current* value defined in ScaleApp class"""
        sm = self.manager
        sm.current = 'start'     
        

    def btn_go(self):
        """Author Necip, Florian Checks necessary login credentials"""
        try:
            for value in ["mqtt_host", "port", "fullTopic"]:
                if self.userIN[value] == "":
                    self.notification("Error - connection not set through missing informations")
        except Exception as e:
            print(e)
            
        sm = self.manager
        sm.current = 'start'


    
    def btn_check_connection(self):
        """Author Florian, Necip Checks if connection credentials set correct and connection can be ethablished"""
        try:
            self.mq = MQTTconnector(shost=self.userIN.get('mqtt_host'),sport=int(self.userIN.get('port')),stopic=self.userIN.get('fullTopic'))
            self.mq.build_connection()
            self.save_values()

        except Exception as e:
            self.notification("Invalid input")

    
    def notification(self, msg: str):
        """Author Florian Notification function to show popup. *msg* means the message to show in the popup"""
        popup = Popup(
        title = msg,
        #content='Cant establish a working connection...',
        size_hint = (None, None),
        size = (500, 300), #size=(Window.width / 3, Window.height / 3),
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
        """Author Florian Switches to configuration panel"""
        sm = self.manager
        sm.current = 'config'



    # Libellen-smoother********************************************   
    def collector_X_Y(self, pos):
        """Author Florian Takes the sensor data Tuple and adds to x/y array respectively"""
        if len(self.arr_of_X) < 6 and len(self.arr_of_Y) < 6:
            self.arr_of_X.append(-1*pos[1])
            self.arr_of_Y.append(pos[0])
        else:
            print(f"collector_X_Y() else-clause = X:{self.arr_of_X} Y:{self.arr_of_Y}")
            self.average_pos(self.arr_of_X, self.arr_of_Y)
            
            
    def average_pos(self, array_x, array_y):
        """Author Florian, Dominik, Gets acceleration data, sends it to label & to the smoothening-process logic"""
        self.pos_x = (round(sum(array_x) / len(array_x), 1)) / 20 + 0.5
        self.pos_y = (round(sum(array_y) / len(array_y), 1)) / 20 + 0.5

        self.arr_of_X = [0, 0]
        self.arr_of_Y = [0, 0]


    def get_acceleration(self, dt):
        '''Author Necip, Dominik, Florian Get accelerometer values, send it to mqtt and show it'''
        try:
            val = accelerometer.acceleration[:3]
            
            if not val == (None, None, None):            
                self.ids.x_label.text = f"X: {-1*val[1]:.3f}"
                self.ids.y_label.text = f"Y: {val[0]:.3f}"
                self.ids.z_label.text = f"Z: {val[2]:.3f}"
                self.collector_X_Y(val)
                dict_values = {"X": f"{-1*val[1]:.3f}","Y": f"{val[0]:.3f}", "Z": f"{val[2]:.3f}" }
                self.mq.send_msg(str(dict_values))
        except Exception as e:
            print(e) 

  

class ScaleApp(App):

    def build(self):
        """Author StartScreen.kv: Florian (Logger-Button and Numbers), Dominik (Libelle and Canvas)
        Author ConfigScreen: Florian"""
        self.icon = 'icon.png'
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
