import queue
from abc import ABC, abstractmethod
from multiprocessing import Process, Queue
from threading import Thread
from typing import List

from adbgateway.config import Config


class Worker(ABC):
    def __init__(self, config: Config):
        self.processes: List[Process] = []
        self.config = config
        self.create_processes()
        self.running = False
        self.thread = Thread(target=self.runner)
        self.q = Queue()

    def runner(self):
        for proc in self.processes:
            proc.start()
        for proc in self.processes:
            proc.join()

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        for proc in self.processes:
            proc.terminate()

    @abstractmethod
    def create_processes(self):
        raise Exception("Not implemented")

    def send_message(self, msg):
        self.q.put(msg)
