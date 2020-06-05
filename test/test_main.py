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

    def tearDown(self):
        shutil.rmtree(self.mock_config_dir_with_out_configs)

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
        pass


if __name__ == "__main__":
    unittest.main()