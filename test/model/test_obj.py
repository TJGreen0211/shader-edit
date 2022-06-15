import unittest

import os

from src.model.obj import ObjectLoader

class TestObj(unittest.TestCase):

    object_path = 'resources/objects/cube.obj'

    def test_load_object(self):
        object_data = ObjectLoader().load_object(self.object_path)
        self.assertEqual(len(object_data), 108)
        self.assertEqual(object_data[0:6], [1.0, -1.0, 1.0, -1.0, -1.0, 1.0])

if __name__ == '__main__':
    unittest.main()
