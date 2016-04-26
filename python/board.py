from timer import Timer


class Board:
    def __init__(self):
        self.High = 1
        self.Low = 0
        self.elements = []
        pass

    def connect(self, element):
        assert isinstance(element, Element), "Only ELement can be connected."
        self.elements.append(element)
        element.onConnect(self)
        return self


class MockBoard(Board):
    def __init__(self):
        Board.__init__(self)
        self.pins = {}
        self.timer = Timer()

    def get(self, pin):
        return self.pins[pin]

    def set(self, pin, value):
        self.pins[pin] = value

    def dump(self):
        for p in self.pins:
            print "%s - %s" % (p, self.get(p))


class Element:
    def __init__(self):
        self.board = None

    def onConnect(self, board):
        self.board = board


