from future_builtins import map, zip
from board import Element
from timer import Timer, Client


class LED(Element):
    def __init__(self, pin, name=''):
        Element.__init__(self)
        self.pin = pin
        self.name = name
        self.client = None

    def on(self):
        self.stopBlink()
        self.board.set(self.pin, self.board.High)

    def stopBlink(self):
        if self.client is not None:
            self.board.timer.unRegister(self.client)
            self.client = None

    def off(self):
        self.stopBlink()
        self.board.set(self.pin, self.board.Low)

    def isOn(self):
        return self.board.get(self.pin) == self.board.High

    def blink(self, interval=100):
        self.stopBlink()
        self.client = Client(interval, lambda x: self.on(), lambda x: self.off())
        self.board.timer.register(self.client)


class LEDS:
    def __init__(self, pins, names=None):
        if names is None:
            names = []
        self.pins = pins
        self.names = names
        if len(names) != 0:
            self.pinNames = zip(pins, names)
        else:
            self.pinNames = zip(pins, range(len(pins)))
        self.leds = list(map(lambda pn: LED(pn[0], pn[1]), self.pinNames))
        assert len(self.leds) == len(pins)


class Digital(Element):
    def __init__(self, pins, name=''):
        Element.__init__(self)
        assert len(pins) == 7, "Only 7 pins supported."
        self.name = name
        self.leds = LEDS(pins)
        self.table = {
            # h:[g,f,e,d,c,b,a]
            0: [0, 1, 1, 1, 1, 1, 1],  # 0
            1: [0, 0, 0, 0, 1, 1, 0],  # 1
            2: [1, 0, 1, 1, 0, 1, 1],  # 2
            3: [1, 0, 0, 1, 1, 1, 1],  # 3
            4: [1, 1, 0, 0, 1, 1, 0],  # 4
            5: [1, 1, 0, 1, 1, 0, 1],  # 5
            6: [1, 1, 1, 1, 1, 0, 1],  # 6
            7: [0, 0, 0, 0, 1, 1, 1],  # 7
            8: [1, 1, 1, 1, 1, 1, 1],  # 8
            9: [1, 1, 0, 1, 1, 1, 1]  # 9
        }

    def on(self, digital):
        ps = self.table[digital]
        for index in range(len(ps)):
            if ps[index] == 1:
                self.leds.leds[index].on()
            else:
                self.leds.leds[index].off()

    def onConnect(self, board):
        Element.onConnect(self, board)
        for l in self.leds.leds:
            board.connect(l)
