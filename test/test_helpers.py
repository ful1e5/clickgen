import logging
import os
import unittest
from unittest.mock import patch

from clickgen import helpers


class TestHelpesMethods(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

        self.orig_cwd = os.getcwd()
        self.dst_dir = 'test'

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_get_looger(self):
        foo_logger = helpers.get_logger('foo')
        self.assertEqual(logging.getLogger('foo'), foo_logger)

    @patch('clickgen.helpers.os.makedirs')
    @patch('clickgen.helpers.os.path.exists')
    def test_create_dir(self, mock_make_dirs, mock_exists):
        mock_exists.return_value = True
        helpers.create_dir('/foo/bar')
        mock_make_dirs.assert_called_with('/foo/bar')

    def test_TemporaryDirectory(self):
        with helpers.TemporaryDirectory() as mock_tmp_dir:
            self.assertTrue(os.path.isdir(mock_tmp_dir))

    @patch('clickgen.helpers.os.chdir')
    def test_cd(self, mock_chdir):
        with helpers.cd(self.dst_dir):
            mock_chdir.reset_mock()
        mock_chdir.assert_called_once_with(self.orig_cwd)

    # TODO:symblinks


if __name__ == '__main__':
    unittest.main()