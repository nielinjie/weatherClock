import threading
import uuid


class Timer:
    def __init__(self):
        self.registers = {}

    def register(self, client):
        t = threading.Timer((client.interval+0.0)/1000.0, lambda x: client.onTime())
        self.registers[client.id] = (client, t)

    def unRegister(self, client):
        (client, timer) = self.registers[client.id]
        timer.cancel()
        del self.registers[client.id]


class Client:
    def __init__(self, interval, *funcs):
        self.interval = interval
        self.funcs = funcs
        self.id = uuid.uuid4()
        self.index = 0

    def onTime(self):
        self.funcs[self.index]()
        self.index += 1
        if self.index == len(self.funcs):
            self.index = 0
