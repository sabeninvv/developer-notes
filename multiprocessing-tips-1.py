import os
from multiprocessing import Process
from time import sleep
from random import uniform
from typing import Any, NoReturn


def get_info(data: Any) -> NoReturn:
    """
    Функция для демонстрации конкурентности в Python на абстракции multiprocessing.Process
    """
    pid = os.getpid()
    to_sleep = uniform(0.2, 1.1)
    sleep(to_sleep)
    print(f"id: {data}, pid: {pid}, sleep: {to_sleep}")


def main() -> NoReturn:
    """
    Объявить процессы с назначенной функцией для обработки,
    запустить процессы, дождаться выполнения
    """
    print("start procs")
    procs = []
    numbers_procs = [i for i in range(20)]

    for num in numbers_procs:
        proc = Process(target=get_info, args=(num, ))
        procs.append(proc)
        proc.start()

    print("to join")
    _ = [proc.join() for proc in procs]


if __name__ == "__main__":
    main()
