#!/usr/bin/env python
# encoding: utf-8
import unittest

from . import assets
from clickgen import configsgen


class TestConfigsgen(unittest.TestCase):

    # tests
    def test_get_cursor_list(self):
        # testing static images list
        mock_static_list = configsgen.get_cursor_list(
            imgs_dir=assets.get_mock_images_path(), animated=False)

        self.assertEqual(mock_static_list, ['mock_static.png'])
