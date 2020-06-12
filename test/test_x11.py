#!/usr/bin/env python
# encoding: utf-8

import os
import shutil
import tempfile
import unittest

from . import assets
from clickgen import x11
from clickgen.x11 import libpath


class TestX11Builder(unittest.TestCase):

    # setup
    def setUp(self):
        self.mock_argv = ['foo', 'bar']
        self.temp_dir = tempfile.mkdtemp()
        self.mock_prefix = assets.mock_config_path
        self.mock_static_out = os.path.join(self.temp_dir, 'mock_static')
        self.mock_animated_out = os.path.join(self.temp_dir, 'mock_animated')

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    # helpers
    def assert_cursor_size(self, path: str):
        self.assertGreater(os.path.getsize(path), 0)

    # tests
    def test_gen_argv_ctypes(self):
        # testing return proper argument class
        mock_result = x11.gen_argv_ctypes(self.mock_argv)
        self.assertEqual(str(mock_result.__class__),
                         "<class 'clickgen.x11.LP_LP_c_char'>")

    def test_generate(self):
        # binary exists
        self.assertTrue(os.path.exists(libpath))

    def test_main(self):
        # testing static cursor
        x11.main(input_config=assets.get_static_mock_config_path(),
                 output_file=self.mock_static_out,
                 prefix=self.mock_prefix)
        self.assert_cursor_size(self.mock_static_out)

        # testing animated cursor
        x11.main(input_config=assets.get_animated_mock_config_path(),
                 output_file=self.mock_animated_out,
                 prefix=self.mock_prefix)
        self.assert_cursor_size(self.mock_animated_out)


if __name__ == '__main__':
    unittest.main()
