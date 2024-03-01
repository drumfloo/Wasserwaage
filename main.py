from math import sqrt
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup
from kivy.core.window import Window
#from plyer import accelerometer
from kivy.uix.screenmanager import ScreenManager, Screen
import json, time
import paho.mqtt.client as mqtt
from mqtt.mqtt_connector import MQTTconnector



class ConfigScreen(Screen):
        
    def __init__(self, **kwargs):
         super(ConfigScreen, self).__init__(**kwargs)
         self.size_hint = (1, 1)
         self.mq = MQTTconnector()

    credentialKeys = ["mqtt_host", "port", "userName", "password", "fullTopic", "intervals", "dimensions"]
    userIN = {}
    popItUp = False
    

    def login_data_fetcher(self, type, value):
        """Fetches login data for mqtt connection. Saved as 
        key:value pairs in a Python dict"""
        self.userIN[type] = value
        print(self.userIN) # DEBUG

    
    def mqtt_handler(self, broker_address, broker_port):
        # sample-data, replace with acceleration data
        topic = "test_topic"
        data = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }
        


# Buttons
    def btn_back(self):
        """Navigate back to *sm.current* value defined in ScaleApp class"""
        print("BACK BUTTON...")# DEBUG
        sm = self.manager
        sm.current = 'start'     
        

    def btn_go(self):
        """Navigates back to scale if login data set and connection correct. Else it 
        shows a popup-hint"""
        self.popItUp = True
        for val in self.credentialKeys:
            if val not in self.userIN:
                self.popItUp = False
                break

        if not self.popItUp:
            popup = Popup(
            title="Something went wrong... there are wrong or missing informations!",
            #content='Cant establish a working connection...',
            size_hint=(None, None),
            size=(250, 100), #size=(Window.width / 3, Window.height / 3),
            auto_dismiss=True,
            )
            # on_press=popup.dismiss
            popup.open()
        else:
            # start giving login credentials to mqtt an switch back to scaler-panel
            sm = self.manager
            sm.current = 'start'

        #self.mqtt_handler(self.userIN['mqtt_host'], self.userIN['port'], self.userIN['UserName'], self.userIN['password'])
        #print(self.userIN['mqtt_host'],self.userIN['port'], self.userIN['UserName'], self.userIN['password'] )

    
    def btn_checkConnection(self):
        """Checks if connection credentials set correct and connection can be ethablished"""
        self.mq.build_connection()
        
        self.save_config()
        
        print("CHECK_CONNECTION...")# DEBUG      


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
        


class StartScreen(Screen):
   
    def btn_config(self):
        """Switches to configuration panel to set mqtt credentials"""
        print("BTN_CONFIG...")
        sm = self.manager
        sm.current = 'config'
    
    def toggle_state(self):
        if ConfigScreen.popItUp == True:
            self.ids.toggle_button.text = 'Logger'
            self.ids.toggle_button.color =  0, 1, 0, 1
            #self.ids.toggle_button.color = 0, 1, 0, 1  # Green text
        # else:
        #     #self.ids.toggle_button.text = 'Logger'
        #     self.ids.toggle_button.color =  0, 1, 0, 1

    def calculate_points(x1, y1, x2, y2, steps=5):
        dx = x2 - x1
        dy = y2 - y1
        dist = sqrt(dx * dx + dy * dy)
        if dist < steps:
            return
        o = []
        m = dist / steps
        for i in range(1, int(m)):
            mi = i / m
            lastx = x1 + dx * mi
            lasty = y1 + dy * mi
            o.extend([lastx, lasty])
        return o





class ScaleApp(App):
    acceleration = 0

    def build(self):        
        Builder.load_file('StartScreen.kv')
        Builder.load_file('ConfigScreen.kv')
        sm = ScreenManager()
        start_screen = StartScreen(name='start')
        config_screen = ConfigScreen(name='config')
        sm.add_widget(start_screen)
        sm.add_widget(config_screen)
        return sm

    # def get_acceleration(self):
    #     accelerometer.enable()
    #     acceleration = accelerometer.acceleration
    #     self.label.text = f"Neigung: {acceleration}"
    #     print(acceleration)



if __name__ == '__main__':
    ScaleApp().run()
    mq = MQTTconnector()
    mq.build_connection()
    mq.send_msg("Sende eine Nachricht")




