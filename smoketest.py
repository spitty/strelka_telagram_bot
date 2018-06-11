import unittest


class Test(unittest.TestCase):
    def test_get_status(self):
        from checker import get_status
        self.assertRaises(ValueError, lambda: get_status('01234567890'))
        # expect no errors


if __name__ == "__main__":
    unittest.main()
