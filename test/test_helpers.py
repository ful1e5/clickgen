import logging
import unittest
from unittest.mock import patch

from clickgen import helpers


class TestHelpesMethods(unittest.TestCase):
    def test_get_looger(self):
        foo_logger = helpers.get_logger('foo')
        self.assertEqual(logging.getLogger('foo'), foo_logger)

    @patch('clickgen.helpers.os.makedirs')
    @patch('clickgen.helpers.os.path.exists')
    def test_create_dir(self, mock_make_dirs, mock_exists):
        mock_exists.return_value = True

        helpers.create_dir('/foo/bar')

        mock_make_dirs.assert_called_with('/foo/bar')


if __name__ == '__main__':
    unittest.main()