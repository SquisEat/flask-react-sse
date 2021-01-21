import json
import logging
import pprint
from threading import Thread
import sseclient
from aiohttp_sse_client import client as sse_client
from requests.exceptions import ChunkedEncodingError, StreamConsumedError, ConnectionError
from urllib3.exceptions import ProtocolError

NUM_CLIENTS = 20

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s')


class Supplierclient(Thread):
    def __init__(self, supplierID):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.supplierID = supplierID
        self.url = f'http://localhost:5001/events?channel=supplierID_{self.supplierID}'
        self.logger.info(f"Initializing supplierID={self.supplierID} with url={self.url}")

        self.logger.info(f"Putting supplierID={supplierID} to idle...")

    """async def run(self):
        while True:
            try:
                async with sse_client.EventSource(self.url) as event_source:
                    try:
                        async for event in event_source:
                            print(event)
                    except ConnectionError:
                        pass
            except ChunkedEncodingError as e:
                print(e)
            except StreamConsumedError as e:
                print(e)"""

    def run(self):
        while True:
            try:
                self.response = Supplierclient.with_requests(self.url)
                self.client = sseclient.SSEClient(self.response)
            except ConnectionError as e:
                self.logger.exception(str(e))
                continue
            except ProtocolError as e:
                self.logger.exception(str(e))
                continue
            try:
                for event in self.client.events():
                    print(json.loads(event.data))
            except ChunkedEncodingError as e:
                self.logger.exception(str(e))
            except StreamConsumedError as e:
                self.logger.exception(str(e))

    @staticmethod
    def with_urllib3(url):
        """Get a streaming response for the given event feed using urllib3."""
        import urllib3
        http = urllib3.PoolManager()
        return http.request('GET', url, preload_content=False)

    @staticmethod
    def with_requests(url):
        """Get a streaming response for the given event feed using requests."""
        import requests
        return requests.get(url, stream=True)


def main():
    threads = []
    for i in range(1, NUM_CLIENTS):
        s = Supplierclient(i)
        s.start()
        threads.append(s)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
