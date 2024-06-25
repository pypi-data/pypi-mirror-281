import unittest
from microGUI.mainloop import MainLoop


class TestMainLoop(unittest.TestCase):

    def setUp(self) -> None:
        self.mainloop = MainLoop()

    def test_running(self):
        self.assertFalse(self.mainloop.running)

        self.mainloop.running = True
        self.assertTrue(self.mainloop.running)

        self.mainloop.running = False
        self.assertFalse(self.mainloop.running)

        self.assertRaises(TypeError, setattr, self.mainloop, "running", 42)

    def test_run(self):
        self.assertFalse(self.mainloop.running)

        self.mainloop.start()
        self.assertTrue(self.mainloop.running)

    def test_stop(self):
        self.assertFalse(self.mainloop.running)

        self.mainloop.running = True
        self.assertTrue(self.mainloop.running)

        self.mainloop.stop()
        self.assertFalse(self.mainloop.running)


if __name__ == '__main__':
    unittest.main()
