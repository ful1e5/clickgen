#!/usr/bin/env python
# encoding: utf-8

import os
import logging
import tempfile

import unittest
from unittest.mock import patch

from clickgen import helpers


class TestHelpesMethods(unittest.TestCase):

    # setup
    def setUp(self):
        logging.disable(logging.CRITICAL)

        self.orig_cwd = os.getcwd()
        self.dst_dir = 'foo'

        self.test_target = os.path.join(tempfile.gettempdir(), 'foo')
        self.test_link_name = os.path.join(tempfile.gettempdir(), 'bar')

    def tearDown(self):
        logging.disable(logging.NOTSET)

    # tests
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

    @patch('clickgen.helpers.os.replace')
    @patch('clickgen.helpers.tempfile.mktemp')
    @patch('clickgen.helpers.os.symlink')
    def test_symblink(self, mock_symlink, mock_temp_link, mock_replace):

        # testing general symbolic link
        helpers.symlink(target=self.test_target,
                        link_name=self.test_link_name,
                        overwrite=False)
        mock_symlink.assert_called_with(self.test_target, self.test_link_name)

        # testing force symbolic link
        tmp_link = '/asdasd'
        mock_temp_link.return_value = tmp_link

        helpers.symlink(target=self.test_target,
                        link_name=self.test_link_name,
                        overwrite=True)
        mock_symlink.assert_called_with(self.test_target, tmp_link)
        mock_replace.assert_called_with(tmp_link, self.test_link_name)


if __name__ == '__main__':
    unittest.main()