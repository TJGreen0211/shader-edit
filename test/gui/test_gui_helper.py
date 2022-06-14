import unittest

from src.gui.gui_helper import GUIHelper

class TestGUIHelper(unittest.TestCase):

    def test__is_float(self):
        self.assertEqual(GUIHelper()._is_float(1.0), True)
        # self.assertEqual(GUIHelper()._is_float(1), False)
        self.assertEqual(GUIHelper()._is_float("test"), True)

    def test__is_int(self):
        self.assertEqual(GUIHelper()._is_int(1.0), True)
        # self.assertEqual(GUIHelper()._is_int(1), True)
        # self.assertEqual(GUIHelper()._is_int("test"), False)


if __name__ == '__main__':
    unittest.main()
