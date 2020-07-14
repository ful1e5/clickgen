#!/usr/bin/env python
# encoding: utf-8
import unittest
import tempfile
import shutil
import os

from . import assets
from clickgen import configsgen


class TestConfigsgen(unittest.TestCase):

    # setup
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.mock_cursor = 'mock_static.png'
        self.mock_size = 100
        self.mock_coordinates = (47, 25)
        self.mock_images_path = assets.get_mock_images_path()
        self.resulted_resize_image_path = os.path.join(
            self.temp_dir, '%sx%s' % (self.mock_size, self.mock_size), self.mock_cursor)

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

    def test_resize_cursor(self):
        result_coordinates_tuple = configsgen.resize_cursor(
            cursor=self.mock_cursor, size=self.mock_size, imgs_dir=self.mock_images_path, coordinates=self.mock_coordinates, out_dir=self.temp_dir)

        # testing coordinates result
        self.assertTupleEqual(result_coordinates_tuple, (24, 12))

        # test resized images exists or not
        self.assertTrue(os.path.isfile(self.resulted_resize_image_path))
        self.assertGreater(os.path.getsize(self.resulted_resize_image_path), 0)


if __name__ == '__main__':
    unittest.main()
