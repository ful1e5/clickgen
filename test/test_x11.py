import ctypes
import unittest
from unittest.mock import patch

from clickgen import x11
from clickgen.x11 import libpath


class TestX11Builder(unittest.TestCase):
    def setUp(self):
        self.test_argv = ['foo', 'bar']

    def test_gen_argv_ctypes(self):
        mock_result = x11.gen_argv_ctypes(self.test_argv)
        self.assertEqual(str(mock_result.__class__),
                         "<class 'clickgen.x11.LP_LP_c_char'>")


if __name__ == '__main__':
    unittest.main()
