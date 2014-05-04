import unittest
import config

class TestConfig(unittest.TestCase):
    def setUp(self):
        with open('harmony.json') as f:
            cfg = f.read()
        self.cfg = config.HarmonyConfig(cfg)

    def test_get_activities(self):
        a = self.cfg.get_activities()
        self.assertEqual(len(a), 5)

if __name__ == '__main__':
    unittest.main()