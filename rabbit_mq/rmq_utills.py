import os
from typing import Tuple
import pika


def init_rmq() -> Tuple[pika.BlockingConnection.BlockingChannel, pika.BlockingConnection]:
    """
    Инициализация pika абстракций (pika.BlockingConnection, pika.BlockingConnection.channel)
    для взаимодействия с RabbitMQ.
    :return:
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RMQ_HOST"),
            port=int(os.getenv("RMQ_PORT")),
            virtual_host=os.getenv("RMQ_VHOST"),
            credentials=pika.PlainCredentials(os.getenv("RMQ_USERNAME"),
                                              os.getenv("RMQ_PASSWORD")
                                              ),
        )
    )
    channel = connection.channel()
    return channel, connection
