import random
import json
import time
from azure.eventhub import EventHubProducerClient, EventData

connection_str = "Endpoint=sb://mysmarthomenamespace.servicebus.windows.net/;SharedAccessKeyName=read_write;SharedAccessKey=*****;EntityPath=mysmarthomeeventhub"
eventhub_name = "MySmartHomeEventHub"

producer = EventHubProducerClient.from_connection_string(
    conn_str=connection_str,
    eventhub_name=eventhub_name  #Pass as a keyword argument
)

def generate_iot_data():
    return {
        "device_id": random.randint(1, 100),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": random.uniform(20, 30),
        "motion": random.choice([True, False]),
        "light_status": random.choice(["ON", "OFF"])
    }

while True:
    iot_data = generate_iot_data()
    event_data = EventData(json.dumps(iot_data)) 
    producer.send_batch([event_data])
    time.sleep(5)  # Send data every 5 seconds
