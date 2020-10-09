from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from cryptography.fernet import Fernet
from multiprocessing import Event
import socket

HOST = '127.0.0.1'
PORT = 10000
SSH_DIR = "$HOME/.ssh"

class ConnectionProcessor:
    def __init__(self, max_workers: int, ssh_key: ):
        self._pool = ThreadPoolExecutor(max_workers=max_workers)
        self._clients = defaultdict(None)
        self._stop = Event()

    def add(self, connection, client_address)
        # Submit the connection with the process method to the pool.
        future = self._pool.submit(
            self.process_connection, connection, client_address)

        # Add extra properties to the future for the cancel hook.
        future._backref = self              # Reference to managing instance
        future._address = client_address    # Client address tied to future
        future._connection = connection     # Accepted connection for processing
        # Add the callback for cleanup.
        future.add_done_callback(self.cleanup_callback)

        # Add future to tracked clients
        self._clients[client_address] = future

    def cleanup_client(self, client_address):
        # May need locking here
        self._clients.pop(client_address, None)

    @staticmethod
    def cleanup_callback(future):
        future._backref.cleanup_client(future._address)

    def process_connection(self, connection, client_address):
        with connection:


    def stop(self):
        self._stop.set()

    def listen(self, socket):
        while not self._stop:
            socket.listen()
            connection, client_address = socket.accept()
            self.add(connection, client_address)