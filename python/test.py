import unittest
import board
from board import Element, MockBoard
from led import LED, Digital


class TestBoard(unittest.TestCase):
    # how to use board
    def test_createBoard(self):
        b = MockBoard()
        self.assertTrue(True)

    def test_connect(self):
        b = MockBoard()
        ele = Element()
        b.connect(ele).connect(Element())
        self.assertTrue(True)

    def test_led(self):
        b = MockBoard()
        led = LED(1)
        b.connect(led)
        led.on()
        self.assertEqual(b.get(1), b.High)
        led.off()
        self.assertEqual(b.get(1), b.Low)

    def test_digital(self):
        b = MockBoard()
        d = Digital(range(1, 8), 'D')
        b.connect(d)
        d.on(8)
        for i in range(1, 8):
            self.assertEqual(b.get(i), b.High)
        d.on(1)
        for i in range(1, 8):
            if i == 5 or i == 6:
                self.assertEqual(b.get(i), b.High)
            else:
                self.assertEqual(b.get(i), b.Low)


class TestUse(unittest.TestCase):
    def test_weather(self):
        b = MockBoard()
        led = LED(8)
        digital = Digital(range(1, 8))
        b.connect(led).connect(digital)
        led.on()
        # begin do some high level business
        led.blink(100)
        self.assertEqual(b.get(8), b.High)
        # begin do some high level business

        led.off()
        self.assertEqual(b.get(8), b.Low)

        digital.on(1)

        for i in range(1, 8):
            if i == 5 or i == 6:
                self.assertEqual(b.get(i), b.High)
            else:
                self.assertEqual(b.get(i), b.Low)


if __name__ == '__main__':
    unittest.main()
