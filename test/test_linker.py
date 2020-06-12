#!/usr/bin/env python
# encoding: utf-8

import os
import logging

import unittest

from clickgen.linker import __main__ as linker


class TestLinker(unittest.TestCase):

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
        # word is similar to directory
        self.assert_to_directory(name='F0o', expect_name='foo')
        # word new to directory
        self.assert_to_directory(name='foo_bar_zoo', expect_name='foo_bar_zoo')

    def test_load_data(self):
        # checking data file extists
        self.assertTrue(os.path.exists(linker.data_file))


if __name__ == "__main__":
    unittest.main()