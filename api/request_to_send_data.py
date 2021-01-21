import logging
import random
from threading import Thread
from time import sleep

import requests

NUM_THREADS = 20
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s')


class RequestClass(Thread):
    def __init__(self, id):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.id = id
        self.url = "http://localhost:5001/send-data"
        self.request_id = 0
        self.logger.info(f"I'm request n°{id}")

    def run(self):
        while True:
            r = requests.post(self.url)
            r.raise_for_status()
            self.logger.info(f"Request_id={self.request_id} from id={self.id} returned = {r.text}")
            sleep_int = random.randint(5, 10)
            self.logger.info(f"ID={self.id} sleeping {sleep_int} seconds")
            sleep(sleep_int)
            self.request_id += 1


def main():
    threads = []
    for i in range(NUM_THREADS):
        r = RequestClass(i)
        r.start()
        threads.append(r)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
