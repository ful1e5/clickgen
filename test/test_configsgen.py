#!/usr/bin/env python
# encoding: utf-8
import unittest
import tempfile
import shutil
import os
from PIL import Image

from . import assets
from clickgen import configsgen


class TestConfigsgen(unittest.TestCase):

    # setup
    def setUp(self):

        self.temp_dir = tempfile.mkdtemp()

        # for test_resize_image
        self.mock_cursor = 'mock_static.png'
        self.mock_size = 100
        self.mock_coordinates = (47, 25)
        self.mock_images_path = assets.get_mock_images_path()
        self.resulted_resize_image_path = os.path.join(
            self.temp_dir, '%sx%s' % (self.mock_size, self.mock_size), self.mock_cursor)

        # for test_write_xcur
        self.mock_config_path = os.path.join(self.temp_dir, 'foo.in')
        self.mock_config_content = ['foo\n', 'bar\n', 'zoo\n']

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    # helpers
    def assert_file_is_valid(self, path: str):
        self.assertTrue(os.path.isfile(path))
        self.assertGreater(os.path.getsize(path), 0)

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
        self.assert_file_is_valid(self.resulted_resize_image_path)

        # test resized image dimensions & type as `.png`
        mock_resize_image_instace = Image.open(self.resulted_resize_image_path)

        self.assertTupleEqual(mock_resize_image_instace.size,
                              (self.mock_size, self.mock_size))
        self.assertEqual(mock_resize_image_instace.mode, 'RGBA')

        mock_resize_image_instace.close()

    def test_write_xcur(self):
        configsgen.write_xcur(
            config_file_path=self.mock_config_path, content=self.mock_config_content)

        self.assert_file_is_valid(self.mock_config_path)


if __name__ == '__main__':
    unittest.main()
