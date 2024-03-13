import paho.mqtt.client as paho
import uuid

class MQTTconnector:
    host = ""
    port = 0
    topic = ""

    def __init__(self, shost="broker.hivemq.com", stopic = "gsog/test/waage", sport=1883) -> None:
        global host
        global port
        global topic
        host = shost
        topic = stopic
        port = sport
        self.client_id = str(uuid.uuid1())


    def build_connection(self):
        global host
        global port
        self.mqtt_client= paho.Client(paho.CallbackAPIVersion.VERSION2 ,self.client_id)
        self.mqtt_client.connect(host,port)

    def send_msg(self, msg):
       global topic
       status,_ = self.mqtt_client.publish(topic, msg, qos=0)
       if status == 0:
        print(f"Send successful")

    def disconnection(self):
       self.mqtt_client.disconnect()
