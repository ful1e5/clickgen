import unittest
import logging

from clickgen import helpers


class TestHelpesMethods(unittest.TestCase):
    def test_get_looger(self):
        foo_logger = helpers.get_logger('foo')
        self.assertEqual(logging.getLogger('foo'), foo_logger)

    def test_create_dir(parameter_list):
        pass


if __name__ == '__main__':
    unittest.main()