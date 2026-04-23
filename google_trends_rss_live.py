import feedparser
from azure.eventhub import EventHubProducerClient, EventData
from datetime import datetime
import json
import time

CONNECTION_STR = "Endpoint=sb://trendhubadi01.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=GuzvWGEK33UHByvPjrSnMnl9m26/SXgYj+AEhM9eBhc="
EVENT_HUB_NAME = "trend-events"
RSS_URL = "https://trends.google.com/trending/rss?geo=IN"

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENT_HUB_NAME
)

while True:
    feed = feedparser.parse(RSS_URL)
    print("\n🔥 LIVE GOOGLE TRENDS (INDIA)\n")

    for entry in feed.entries[:10]:
        keyword = entry.title

        # Extract real search volume from ht:approx_traffic tag
        search_volume_raw = entry.get("ht_approx_traffic", "0")
        # Clean it — Google sends values like "1K+", "200+", "10K+"
        search_volume_str = search_volume_raw.replace("K+", "000").replace("+", "").strip()
        try:
            search_volume = int(search_volume_str)
        except:
            search_volume = 100  # fallback only

        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "keyword": keyword,
            "search_volume": search_volume,   # ← real value now
            "mentions": 1
        }

        batch = producer.create_batch()
        batch.add(EventData(json.dumps(event)))
        producer.send_batch(batch)

        print(f"Sent: {keyword} | Volume: {search_volume}")

    time.sleep(30)