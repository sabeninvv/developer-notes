import time
import json
from rmq_utills import *


def callback(ch, method, properties, body: bytes):
    parsed_msg = json.loads(body.decode("utf-8"))
    print(f"Task received: {parsed_msg}")
    time.sleep(1)
    print(f"Task processed")
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    channel, connection = init_rmq()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=os.getenv("RMQ_QUEUE_NAME"),
        on_message_callback=callback)
    channel.start_consuming()
