import unittest
import config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.cfg = config.HarmonyConfig('harmony.json')

    def test_get_activities(self):
        a = self.cfg.get_activities()
        self.assertEqual(len(a), 5)
        self.assertEqual(a[-1], 'PowerOff')
        self.assertEqual(a[5337061], 'Play a Game')

    def test_get_devices(self):
        d = self.cfg.get_devices()
        self.assertEqual(len(d), 5)
        self.assertEqual(d[13603402], 'Microsoft Xbox 360')

if __name__ == '__main__':
    unittest.main()