import os
import shutil
import tempfile

import unittest
from unittest.mock import patch

from clickgen import x11
from clickgen.x11 import libpath
import assets


class TestX11Builder(unittest.TestCase):
    def setUp(self):
        self.mock_argv = ['foo', 'bar']
        self.temp_dir = tempfile.mkdtemp()
        self.mock_prefix = assets.mock_config_path
        self.mock_static_out = os.path.join(self.temp_dir, 'mock_static')
        self.mock_animate_out = os.path.join(self.temp_dir, 'mock_static')

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

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

        self.assertGreater(os.stat(self.mock_static_out).st_size, 0)


if __name__ == '__main__':
    unittest.main()
