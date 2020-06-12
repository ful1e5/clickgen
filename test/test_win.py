#!/usr/bin/env python
# encoding: utf-8

import os
import shutil
import tempfile
import unittest

from . import assets
from clickgen import win


class TestWinBuilder(unittest.TestCase):

    # setup
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.mock_prefix = assets.mock_config_path
        self.mock_static_out = os.path.join(self.temp_dir, 'mock_static.cur')
        self.mock_animated_out = os.path.join(self.temp_dir,
                                              'mock_animated.ani')

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    # helpers
    def assert_cursor_size(self, path: str):
        self.assertGreater(os.path.getsize(path), 0)

    # tests
    # TODO: More to test here
    def test_main(self):
        # testing static cursor
        win.main(input_config=assets.get_static_mock_config_path(),
                 output_file=self.mock_static_out,
                 prefix=self.mock_prefix)
        self.assert_cursor_size(self.mock_static_out)

        # testing animated cursor
        win.main(input_config=assets.get_animated_mock_config_path(),
                 output_file=self.mock_animated_out,
                 prefix=self.mock_prefix)
        self.assert_cursor_size(self.mock_animated_out)


if __name__ == '__main__':
    unittest.main()
