import unittest
from sai_krrish.greet import greet


class TestGreeter(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Jello"), "Hello, Jello!")


if __name__ == '__main__':
    unittest.main()
