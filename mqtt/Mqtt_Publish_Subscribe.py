import paho.mqtt.client as paho
import time
import uuid

broker="broker.hivemq.com"
port=1883
topic = "gsog/test/waage"

def on_publish(client,userdata,result): #create function for callback
    print("data published \n")
    pass
    
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

client_id = str(uuid.uuid1())
print(client_id)
mqtt_client= paho.Client(paho.CallbackAPIVersion.VERSION2 ,client_id)    # create client object
mqtt_client.on_publish = on_publish    # assign function to callback
mqtt_client.connect(broker,port)
print("Subscribing to topic",topic)
mqtt_client.subscribe(topic,qos=0)
mqtt_client.on_message=on_message      # attach function to callback
mqtt_client.loop_start()               #start the loop

for i in range(5):
    msg = f"Demo: {i:02d}"
    status,_ = mqtt_client.publish("gsog/test/waage",msg,qos=0)
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    time.sleep(1)
    
mqtt_client.loop_stop()
mqtt_client.disconnect()
print("MQTT Client stopped")
