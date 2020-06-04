
import logging
import unittest

import assets
from clickgen import template


class TestTemplate(unittest.TestCase):

    # setup
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    # tests
    def test_main(self):
        pass


if __name__ == '__main__':
    unittest.main()
