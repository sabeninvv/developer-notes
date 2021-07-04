import os
from multiprocessing import Process, Queue
from _queue import Empty
from time import sleep
from random import uniform
from typing import Any, NoReturn


def get_info(data: Any) -> NoReturn:
    """
    Функция для демонстрации конкурентности в Python на абстракциях
    multiprocessing.Process, multiprocessing.Queue
    """
    pid = os.getpid()
    to_sleep = uniform(0.2, 1.1)
    sleep(to_sleep)
    print(f"id: {data}, pid: {pid}, sleep: {to_sleep}")


def put_in_queue(data: Any, queue: Queue) -> NoReturn:
    """
    Поместить data в очередь queue
    """
    queue.put(data)
    print(f"Put id: {data} to queue")


def get_from_queue(queue: Queue) -> NoReturn:
    """
    Забрать data из очереди queue,
    обработать полученную data в функции get_info
    """
    while True:
        try:
            data = queue.get(timeout=.5)
            get_info(data=data)
            print(f"Get id: {data}")
        except Empty:
            print(f"Sleep. Await")
            sleep(.5)


def main() -> NoReturn:
    """
    Объявить Очередь.
    Объявить и запустить процессы, которые будут складывать данные в Очередь.
    Объявить и запустить процесс вычитывающий из Очереди данные и обрабатывающий их.
    """
    queue = Queue()
    numbers_proc2queue = [i for i in range(10)]
    print("Start put processes to queue", end="\n\n")
    _ = [Process(target=put_in_queue, args=(num, queue)).start() for num in numbers_proc2queue]

    print("Start process in queue", end="\n\n")
    proc_queue = Process(target=get_from_queue, args=(queue,))
    proc_queue.start()
    print("Join process queue", end="\n\n")
    proc_queue.join()


if __name__ == "__main__":
    main()
