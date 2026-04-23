from pytrends.request import TrendReq
from azure.eventhub import EventHubProducerClient, EventData
from datetime import datetime
import json
import time

CONNECTION_STR = "your_eventhub_connection_string"
EVENT_HUB_NAME = "trend-events"

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENT_HUB_NAME
)

pytrends = TrendReq(hl='en-US', tz=330)

keywords = ["IPL", "RCB", "Virat Kohli", "Dhoni"]

while True:
    pytrends.build_payload(keywords, timeframe='now 1-H')
    data = pytrends.interest_over_time()

    latest = data.iloc[-1]

    for keyword in keywords:
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "keyword": keyword,
            "mentions": int(latest[keyword]),
            "engagement": int(latest[keyword]) * 100
        }

        batch = producer.create_batch()
        batch.add(EventData(json.dumps(event)))
        producer.send_batch(batch)

        print("Sent:", event)

    time.sleep(60)