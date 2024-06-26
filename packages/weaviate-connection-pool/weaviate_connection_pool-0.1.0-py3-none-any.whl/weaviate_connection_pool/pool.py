from queue import PriorityQueue, Full, Empty
from weaviate import Client, exceptions as weaviate_exceptions
from threading import Lock


class WeaviateConnectionPool:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(WeaviateConnectionPool, cls).__new__(cls)
                cls._instance._initialize_pool(*args, **kwargs)
        return cls._instance

    def _initialize_pool(
        self, url, auth_client_secret=None, pool_size=5, waiting_time_out=300
    ):
        self._queue = PriorityQueue(maxsize=pool_size)
        self._url = url
        self._auth_client_secret = auth_client_secret
        self._pool_size = pool_size
        self.waiting_time_out = waiting_time_out

    def _create_new_client(self):
        try:
            return Client(url=self._url, auth_client_secret=self._auth_client_secret)
        except weaviate_exceptions.ClientError as e:
            raise ConnectionError(f"Failed to create Weaviate client: {e}")

    def get_client(self):
        try:
            if self._queue.empty() and self._queue.qsize() < self._pool_size:
                client = self._create_new_client()
                self._queue.put_nowait(client)
                return client
            return self._queue.get(timeout=self.waiting_time_out)
        except Full:
            raise Exception("The client pool limit is full. Cannot add more clients.")
        except Empty:
            raise TimeoutError(
                "Connection time out error. Unable to get a client from the pool."
            )
        except Exception as e:
            raise Exception(f"Unexpected error getting a client from the pool: {e}")

    def release_client(self, client: Client):
        try:
            if not self._queue.full():
                self._queue.put_nowait(client)
            else:
                # Properly handle client cleanup if needed
                # Assuming client has a close method for cleanup
                try:
                    client._connection.close()
                except AttributeError:
                    pass  # Client doesn't have a close method
        except Full:
            # Log or handle the case when the queue is unexpectedly full
            pass
        except Exception as e:
            raise Exception(f"Unexpected error releasing the client: {e}")
