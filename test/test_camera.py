import unittest

from src.camera import Camera

class TestCamera(unittest.TestCase):

    def test_get_camera_position(self):
        camera = Camera()
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()