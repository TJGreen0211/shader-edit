import unittest

from src.gui.gui_helper import GUIHelper

class TestGUIHelper(unittest.TestCase):

    def test__is_float(self):
        self.assertEqual(GUIHelper()._is_float(1.0), True)
        # self.assertEqual(GUIHelper()._is_float(1), False)
        self.assertEqual(GUIHelper()._is_float("test"), True)

    def test__is_int(self):
        self.assertEqual(GUIHelper()._is_int(1.0), True)
        self.assertEqual(GUIHelper()._is_int(1), True)
        self.assertEqual(GUIHelper()._is_int("test"), False)

    def test__is_numeric(self):
        self.assertEqual(GUIHelper()._is_numeric(1.0), True)
        self.assertEqual(GUIHelper()._is_numeric("test"), False)
        self.assertEqual(GUIHelper()._is_numeric("1"), True)
        self.assertEqual(GUIHelper()._is_numeric("1.0"), True)

    def test_parse_uniforms(self):
        uniform1f_dict = {'type': 'glUniform1f', 'value': [1.0]}
        uniform2f_dict = {'type': 'glUniform2f', 'value': [1.0, 1.0]}
        uniform3f_dict = {'type': 'glUniform3f', 'value': [1.0, 1.0, 1.0]}
        self.assertEqual(GUIHelper().parse_uniforms('test', '1.0'), uniform1f_dict)
        self.assertEqual(GUIHelper().parse_uniforms('test', '1.0, 1.0'), uniform2f_dict)
        self.assertEqual(GUIHelper().parse_uniforms('test', '1.0, 1.0, 1.0'), uniform3f_dict)

if __name__ == '__main__':
    unittest.main()
