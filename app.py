from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup
from kivy.core.window import Window
#from plyer import accelerometer
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import paho.mqtt.client as mqtt

from kivy.uix.popup import Popup

class ConfigScreen(Screen):
        
    # def __init__(self, **kwargs):
    #     super(ConfigScreen, self).__init__(**kwargs)
    #     self.size_hint = (1, 1)
    credentialKeys = ["mqtt_host", "port", "userName", "password", "fullTopic", "intervals", "dimensions"]
    userIN = {}

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
        client = mqtt.Client()
        client.connect(broker_address, broker_port)
        jsonData = json.dumps(data)
        client.publish(topic, jsonData)


    
    def show_popup(self, infoMsg):
        popupWindow = Popup(title=infoMsg, size_hint=(None,None),size=(400,200)) 
        popupWindow.open()


# Buttons
    def btn_back(self):
        """Navigate back to *sm.current* value defined in ScaleApp class"""
        print("BACK BUTTON...")# DEBUG
        sm = self.manager
        sm.current = 'start'     
        

    def btn_go(self):
        """Navigates back to scale if login data set and connection correct."""
        for credential in self.credentialKeys:
            if credential not in self.userIN:
                self.show_popup("Fehlerhafte MQTT Daten")            
            else:
                self.btn_checkConnection(self.userIN)
                sm = self.manager
                sm.current = 'start'
        

        #self.mqtt_handler(self.userIN['mqtt_host'], self.userIN['port'], self.userIN['UserName'], self.userIN['password'])
        #print(self.userIN['mqtt_host'],self.userIN['port'], self.userIN['UserName'], self.userIN['password'] )

    
    def btn_checkConnection(self, loginData):
        """Checks if connection credentials set correct and connection can be ethablished"""
        print("CHECK_CONNECTION...")# DEBUG        


class StartScreen(Screen):
   
    def btn_config(self):
        """Switches to configuration panel to set mqtt credentials"""
        print("BTN_CONFIG...")
        sm = self.manager
        sm.current = 'config'
    
    



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



