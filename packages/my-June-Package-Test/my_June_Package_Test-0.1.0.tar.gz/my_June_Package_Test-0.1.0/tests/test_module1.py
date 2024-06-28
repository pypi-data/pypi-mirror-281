import unittest
from my_June_Package_Test.module1 import my_function

class TestModule1(unittest.TestCase):

    def test_my_function(self):
        self.assertEqual(my_function(), "Hello, world!")

if __name__ == '__main__':
    unittest.main() 
