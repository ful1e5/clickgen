import logging

import unittest


class TestLinke(unittest.TestCase):

    # setup
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_match_to_directory(self):
        pass


if __name__ == "__main__":
    unittest.main()