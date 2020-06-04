import unittest

import assets
from clickgen import win


class TestWinBuilder(unittest.TestCase):

    # setup
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # helpers
    def assert_cursor_size(self, path: str):
        self.assertGreater(os.path.getsize(path), 0)

    # tests
    def test_main(self):
        pass


if __name__ == '__main__':
    unittest.main()
