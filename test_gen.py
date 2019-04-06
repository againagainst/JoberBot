import unittest
import configparser

import gen


class BotTest(unittest.TestCase):
    def test_gen(self):
        self.assertIsNotNone(gen.sloganmaker.make_slogan())

    def test_config(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.assertIsNotNone(config["telegram"]["token"])


if __name__ == "__main__":
    unittest.main()
