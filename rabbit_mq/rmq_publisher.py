import json
from uuid import uuid4
from rmq_utills import *


if __name__ == "__main__":
    channel, connection = init_rmq()
    channel.queue_declare(queue=os.getenv("RMQ_QUEUE_NAME"), durable=True)

    client_dict = {
        str(uuid4()): {
            "url": "https://ya.ru",
            "groupId": 23,
            "etc": 333
        }
    }
    str_message = json.dumps(client_dict)
    bts_message = bytes(str_message, "utf-8")

    channel.basic_publish(exchange="",
                          routing_key=os.getenv("RMQ_QUEUE_NAME"),
                          body=bts_message,
                          properties=pika.BasicProperties(delivery_mode=2)
                          )
    connection.close()
