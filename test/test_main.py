import shutil
import tempfile

import unittest

from assets import __main__ as assets


class TestMain(unittest.TestCase):
    # setup
    def setUp(self):
        self.mock_config_dir_with_configs = assets.mock_config_path
        self.mock_config_dir_with_out_configs = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.mock_config_dir_with_out_configs)

    # test
    def test_get_config(self):
        pass


if __name__ == "__main__":
    unittest.main()