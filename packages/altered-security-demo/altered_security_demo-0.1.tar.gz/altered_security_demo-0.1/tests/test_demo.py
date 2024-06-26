import unittest
from altersec.demo import demo_function

class TestDemoFunction(unittest.TestCase):
    def test_demo_function(self):
        # This test will just call the function to ensure it runs without errors.
        # Since it shows a messagebox and opens calculator, we are not asserting anything.
        demo_function()

if __name__ == '__main__':
    unittest.main()
