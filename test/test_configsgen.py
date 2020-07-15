#!/usr/bin/env python
# encoding: utf-8

import unittest
import tempfile
import shutil
import logging
import filecmp
import os
from PIL import Image

from . import assets
from clickgen import configsgen


class TestConfigsgen(unittest.TestCase):

    # setup
    def setUp(self):
        logging.disable(logging.CRITICAL)

        self.temp_dir = tempfile.mkdtemp()

        # for test_resize_image
        self.mock_cursor = 'mock_static.png'
        self.mock_size = 100
        self.mock_coordinates = (47, 25)
        self.mock_images_path = assets.mock_images_path
        self.resulted_resize_image_path = os.path.join(
            self.temp_dir, '%sx%s' % (self.mock_size, self.mock_size), self.mock_cursor)

        # for test_write_xcur
        self.mock_config_path = os.path.join(self.temp_dir, 'foo.in')
        self.mock_config_content = ['foo\n', 'bar\n', 'zoo\n']

        # for test_generate_static_cursor
        # 📝 Note : doen't change size that Fail Some test
        self.mock_sizes = [50, 28]
        self.mock_hotspots = assets.get_mock_hotspots()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        logging.disable(logging.NOTSET)

    # helpers
    def assert_file_is_valid(self, path: str):
        self.assertTrue(os.path.isfile(path))
        self.assertGreater(os.path.getsize(path), 0)

    def assert_image_size(self, img_path: str, size: int):
        mock_resize_image_instace = Image.open(img_path)

        self.assertTupleEqual(mock_resize_image_instace.size,
                              (size, size))
        self.assertEqual(mock_resize_image_instace.mode, 'RGBA')

        mock_resize_image_instace.close()

    # tests
    def test_get_cursor_list(self):
        # testing static images list
        mock_static_list = configsgen.get_cursor_list(
            imgs_dir=assets.mock_images_path, animated=False)

        self.assertEqual(mock_static_list, ['mock_static.png'])

        # testing animated images list
        mock_animated_list = configsgen.get_cursor_list(
            imgs_dir=assets.mock_images_path, animated=True)

        self.assertEqual(mock_animated_list, [['mock_animated_1-01.png', 'mock_animated_1-02.png'], [
            'mock_animated_2-01.png', 'mock_animated_2-02.png']])

    def test_resize_cursor(self):
        # 🧪 TEST FOR COORDINATORS
        result_coordinates_tuple = configsgen.resize_cursor(
            cursor=self.mock_cursor, size=self.mock_size, imgs_dir=self.mock_images_path, coordinates=self.mock_coordinates, out_dir=self.temp_dir)

        # testing coordinates result
        self.assertTupleEqual(result_coordinates_tuple, (24, 12))

        # 🧪 TEST FOR `NONE` COORDINATORS
        result_coordinates_tuple = configsgen.resize_cursor(
            cursor=self.mock_cursor, size=self.mock_size, imgs_dir=self.mock_images_path, coordinates=None, out_dir=self.temp_dir)

        # testing coordinates result
        self.assertTupleEqual(result_coordinates_tuple,
                              (self.mock_size / 2, self.mock_size / 2))

        # test resized images exists or not
        self.assert_file_is_valid(self.resulted_resize_image_path)

        # test resized image dimensions & type as `.png`
        self.assert_image_size(
            img_path=self.resulted_resize_image_path, size=self.mock_size)

    def test_write_xcur(self):
        configsgen.write_xcur(
            config_file_path=self.mock_config_path, content=self.mock_config_content)

        self.assert_file_is_valid(self.mock_config_path)

        # testing config file content are sorted & '\n' trimdown from a last line
        with open(self.mock_config_path, 'r') as mock_config:
            mock_content = mock_config.readlines()
            self.assertListEqual(mock_content, ['bar\n', 'foo\n', 'zoo'])

    def test_generate_static_cursor(self):
        # test with `None` Hotspots
        configsgen.generate_static_cursor(
            imgs_dir=self.mock_images_path, out_dir=self.temp_dir, sizes=self.mock_sizes, hotspots=None)

        # testing generated sized directory structure
        for size in self.mock_sizes:
            # have size direcory
            size_dir = '%sx%s' % (size, size)
            self.assertIn(size_dir, os.listdir(self.temp_dir))

            size_dir_path = os.path.join(self.temp_dir, size_dir)

            images_list: [str] = assets.get_mock_static_images_list()

            # have resized images
            self.assertListEqual(images_list, os.listdir(size_dir_path))

            # test resized image dimensions & type as `.png`
            for image in images_list:
                img_path = os.path.join(size_dir_path, image)
                self.assert_image_size(img_path=img_path, size=size)

        # testing .in config file
        result_config_path = os.path.join(self.temp_dir, 'mock_static.in')
        with open(result_config_path, 'r') as file:
            content = file.read()

            for size in self.mock_sizes:
                expect_line: str = '%s %s %s %sx%s/mock_static.png' % (
                    size, size // 2, size // 2, size, size)
                self.assertTrue(expect_line in content)

        # test with `Mock` Hotspots
        configsgen.generate_static_cursor(
            imgs_dir=self.mock_images_path, out_dir=self.temp_dir, sizes=self.mock_sizes, hotspots=self.mock_hotspots)

        # testing .in config file
        # 📝 Note : Hard Coded test. size doesn't affect this test
        result_config_path = os.path.join(self.temp_dir, 'mock_static.in')
        with open(result_config_path, 'r') as file:
            content = file.read()

            for size in self.mock_sizes:
                expect_line: str = '28 2 2 28x28/mock_static.png'
                self.assertTrue(expect_line in content)

                expect_line: str = '50 3 3 50x50/mock_static.png'
                self.assertTrue(expect_line in content)

    def test_generate_animated_cursor(self):
        # test with `None` Hotspots
        configsgen.generate_animated_cursor(
            imgs_dir=self.mock_images_path, out_dir=self.temp_dir, sizes=self.mock_sizes, hotspots=None)

        # testing generated sized directory structure
        for size in self.mock_sizes:
            # have size direcory
            size_dir = '%sx%s' % (size, size)
            self.assertIn(size_dir, os.listdir(self.temp_dir))

            size_dir_path = os.path.join(self.temp_dir, size_dir)

            images_list: [str] = assets.get_mock_animated_images_list()

            gen_list = sorted(os.listdir(size_dir_path))

            # have resized images
            self.assertListEqual(images_list, gen_list)

            # test resized image dimensions & type as `.png`
            for image in images_list:
                img_path = os.path.join(size_dir_path, image)
                self.assert_image_size(img_path=img_path, size=size)

        # testing .in config file
        result_config_path = os.path.join(self.temp_dir, 'mock_animated_1.in')
        with open(result_config_path, 'r') as file:
            content = file.read()

            expect_line: str = '28 14 14 28x28/mock_animated_1-01.png 20\n28 14 14 28x28/mock_animated_1-02.png 20'
            self.assertTrue(expect_line in content)

        # test with `Mock` Hotspots
        configsgen.generate_animated_cursor(
            imgs_dir=self.mock_images_path, out_dir=self.temp_dir, sizes=self.mock_sizes, hotspots=self.mock_hotspots)

        # testing .in config file
        # 📝 Note : Hard Coded test. size doesn't affect this test
        result_config_path = os.path.join(self.temp_dir, 'mock_animated_1.in')
        with open(result_config_path, 'r') as file:
            content = file.read()

            expect_line: str = '28 2 2 28x28/mock_animated_1-01.png 20\n28 2 2 28x28/mock_animated_1-02.png 20\n50 3 3 50x50/mock_animated_1-01.png 20\n50 3 3 50x50/mock_animated_1-02.png 20'
            self.assertTrue(expect_line in content)


if __name__ == '__main__':
    unittest.main()
