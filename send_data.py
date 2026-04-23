from azure.eventhub import EventHubProducerClient, EventData
import json
import time
import random
from datetime import datetime

CONNECTION_STR = "Endpoint=sb://trendhubadi01.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=GuzvWGEK33UHByvPjrSnMnl9m26/SXgYj+AEhM9eBhc="
EVENT_HUB_NAME = "trend-events"

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENT_HUB_NAME
)

keywords = ["IPL", "RCB", "Virat", "Dhoni", "Cricket"]

while True:
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "keyword": random.choice(keywords),
        "mentions": random.randint(50, 100),
        "engagement": random.randint(1000, 10000)
    }

    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData(json.dumps(data)))

    producer.send_batch(event_data_batch)

    print("Sent:", data)

    time.sleep(5)