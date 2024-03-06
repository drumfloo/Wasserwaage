import paho.mqtt.client as paho
import uuid

class MQTTconnector:
    def __init__(self, host="broker.hivemq.com", topic = "gsog/test/waage", port=1883) -> None:
        self.host = host
        self.topic = topic
        self.port = port
        self.client_id = str(uuid.uuid1())


    def build_connection(self):
        self.mqtt_client= paho.Client(paho.CallbackAPIVersion.VERSION2 ,self.client_id)
        self.mqtt_client.connect(self.host,self.port)

    def send_msg(self, msg):
       status,_ = self.mqtt_client.publish(self.topic, msg, qos=0)
       if status == 0:
        print(f"Send successful")

    def disconnection(self):
       self.mqtt_client.disconnect()
