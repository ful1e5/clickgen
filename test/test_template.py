#!/usr/bin/env python
# encoding: utf-8

import os
import shutil
import logging
import tempfile

import unittest

from . import assets
from clickgen.template import __main__ as template


class TestTemplate(unittest.TestCase):

    # setup
    def setUp(self):
        logging.disable(logging.CRITICAL)

        self.mock_dir = tempfile.mkdtemp()
        self.mock_cursor_file_path = os.path.join(self.mock_dir,
                                                  'cursor.theme')
        self.mock_index_file_path = os.path.join(self.mock_dir, 'index.theme')
        self.mock_name = 'foo'
        self.mock_comment = 'foo bar'

    def tearDown(self):
        logging.disable(logging.NOTSET)

        shutil.rmtree(self.mock_dir)

    # helpers
    def assert_word_in_file(self, file: str, word: str):
        with open(file, 'r') as f:
            content = f.read()
            self.assertTrue(word in content)

    # tests
    def test_have_templates_files(self):
        self.assertTrue(os.path.exists(template.cursor_file_path))
        self.assertTrue(os.path.exists(template.index_file_path))

    def test_create_x11_template_without_comments(self):
        template.create_x11_template(name=self.mock_name,
                                     dir=self.mock_dir,
                                     comment='')
        # testing cursor.theme
        self.assert_word_in_file(file=self.mock_cursor_file_path,
                                 word='Name=foo')

        # testing index.theme
        self.assert_word_in_file(file=self.mock_index_file_path,
                                 word='Name=foo')
        self.assert_word_in_file(file=self.mock_index_file_path,
                                 word='Comment=foo cursor theme')

    def test_create_x11_template_with_comments(self):
        template.create_x11_template(name=self.mock_name,
                                     dir=self.mock_dir,
                                     comment=self.mock_comment)
        # testing cursor.theme
        self.assert_word_in_file(file=self.mock_cursor_file_path,
                                 word='Name=foo')

        # testing index.theme
        self.assert_word_in_file(file=self.mock_index_file_path,
                                 word='Name=foo')
        self.assert_word_in_file(file=self.mock_index_file_path,
                                 word='Comment=foo bar')


if __name__ == '__main__':
    unittest.main()
