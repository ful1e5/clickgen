import os
import shutil
import tempfile

import unittest

from clickgen import __main__ as clickgen
from assets import __main__ as assets


class TestMain(unittest.TestCase):
    # setup
    def setUp(self):
        self.mock_config_dir_with_configs = assets.mock_config_path
        self.mock_config_dir_with_out_configs = tempfile.mkdtemp()
        self.mock_config_path = assets.mock_config_path
        self.mock_out_path = tempfile.mkdtemp()
        self.mock_name = 'foo'
        self.foo_dir_path = os.path.join(self.mock_out_path, 'foo')
        self.foo_archive_path = os.path.join(self.mock_out_path, 'foo.tar')

    def tearDown(self):
        shutil.rmtree(self.mock_config_dir_with_out_configs)
        shutil.rmtree(self.mock_out_path)

    # helpers
    def assert_cur_name(self, config: str, type: str, expect_ext: str):
        ext = clickgen.get_cur_name(config, type)

        self.assertEqual(ext, expect_ext)

    # test
    def test_get_config(self):
        # testing with assets dir,have 2 config files
        mock_configs = clickgen.get_configs(
            dir=self.mock_config_dir_with_configs)
        self.assertEqual(len(mock_configs), 2)

        # testing with empty dir
        mock_configs = clickgen.get_configs(
            dir=self.mock_config_dir_with_out_configs)
        self.assertEqual(len(mock_configs), 0)

    def test_is_animated(self):
        # testing config file with aimation
        self.assertTrue(
            clickgen.is_animated(
                config=assets.get_animated_mock_config_path()))

        # testing config file without aimation
        self.assertFalse(
            clickgen.is_animated(config=assets.get_static_mock_config_path()))

    def test_get_cur_name(self):
        # window extensions
        self.assert_cur_name(config=assets.get_animated_mock_config_path(),
                             type='win',
                             expect_ext='mock_animated.ani')
        self.assert_cur_name(config=assets.get_static_mock_config_path(),
                             type='win',
                             expect_ext='mock_static.cur')

        # x11 extensions
        self.assert_cur_name(config=assets.get_animated_mock_config_path(),
                             type='x11',
                             expect_ext='mock_animated')
        self.assert_cur_name(config=assets.get_static_mock_config_path(),
                             type='x11',
                             expect_ext='mock_static')

    def test_x11_dir_struc(self):
        # testing x11 with directory
        print('\n🧪 Testing x11 directory Structure')
        clickgen.main(name=self.mock_name,
                      config_dir=self.mock_config_path,
                      out_path=self.mock_out_path,
                      x11=True)

        # checking cursor dir exists
        self.assertTrue(os.path.exists(self.foo_dir_path))

        mock_x11_dir = os.path.join(self.foo_dir_path, 'x11')
        self.assertTrue(os.path.exists(mock_x11_dir))

        expect_dir_struc = ['cursor.theme', 'cursors', 'index.theme']
        self.assertEqual(os.listdir(mock_x11_dir), expect_dir_struc)

        mock_cursor_dir = os.path.join(mock_x11_dir, 'cursors')
        self.assertGreater(len(os.listdir(mock_cursor_dir)), 0)

    def test_win_dir_struc(self):
        # testing win with directory
        print('\n🧪 Testing win directory Structure')
        clickgen.main(name=self.mock_name,
                      config_dir=self.mock_config_path,
                      out_path=self.mock_out_path,
                      win=True)

        # checking cursor dir exists
        self.assertTrue(os.path.exists(self.foo_dir_path))

        mock_win_dir = os.path.join(self.foo_dir_path, 'win')
        self.assertTrue(os.path.exists(mock_win_dir))


if __name__ == "__main__":
    unittest.main()