#!/usr/bin/env python
# encoding: utf-8
import unittest
import tempfile
import shutil

from . import assets
from clickgen import configsgen


class TestConfigsgen(unittest.TestCase):

    # setup
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    # tests
    def test_get_cursor_list(self):
        # testing static images list
        mock_static_list = configsgen.get_cursor_list(
            imgs_dir=assets.get_mock_images_path(), animated=False)

        self.assertEqual(mock_static_list, ['mock_static.png'])

        # testing animated images list
        mock_animated_list = configsgen.get_cursor_list(
            imgs_dir=assets.get_mock_images_path(), animated=True)

        self.assertEqual(mock_animated_list, [['mock_animated_1-01.png', 'mock_animated_1-02.png'], [
            'mock_animated_2-01.png', 'mock_animated_2-02.png']])
