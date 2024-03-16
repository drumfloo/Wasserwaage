import paho.mqtt.client as paho
import uuid

class MQTTconnector:
    host = ""
    port = 0
    topic = ""
    mqtt_client = None

    def __init__(self, shost="broker.hivemq.com", stopic = "gsog/test/waage", sport=1883) -> None:
        global host
        global port
        global topic
        host = shost
        topic = stopic
        port = sport
        self.client_id = str(uuid.uuid1())


    def build_connection(self):
        """Author Necip Builds connection and returns boolean if its successful"""
        try:
            global host
            global port
            global mqtt_client
            mqtt_client= paho.Client(paho.CallbackAPIVersion.VERSION2 ,self.client_id)
            retvalue = mqtt_client.connect(host,port)
            return True
        except Exception as e:
            print("Exception in build_connection")
            print(e)
            return False

    def send_msg(self, msg):
        """Author Necip Publishing message"""
        try:
            global topic
            global mqtt_client
    
            status,_ = mqtt_client.publish(topic, msg, qos=0)
            if status == 0:
                print(f"Send successfull")
        except Exception as e:
            print("Exception in send_msg")
            print(e)

    def disconnection(self):
       """Author Necip Disconnects client from Server"""
       global mqtt_client
       mqtt_client.disconnect()
