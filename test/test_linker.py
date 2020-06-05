import logging

import unittest

from clickgen.linker import __main__ as linker


class TestLinke(unittest.TestCase):

    # setup
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.mock_directory = ['foo', 'bar', 'zoo']

    def tearDown(self):
        logging.disable(logging.NOTSET)

    # helpers
    def assert_to_directory(self, name: str, expect_name: str):
        mock_result = linker.match_to_directory(name,
                                                directory=self.mock_directory)
        self.assertEqual(mock_result, expect_name)

    # tests
    def test_match_to_directory(self):
        self.assert_to_directory(name='F0o', expect_name='foo')
        # self.assert_to_mock_directory(name='F0o', expect_name='foo')


if __name__ == "__main__":
    unittest.main()