"""Helper functions for the GUI."""


class GUIHelper():
    """Functions used in the GUI class to help parse uniform data."""

    def __init__(self):
        """Constructor."""
        pass

    def _is_float(self, x):
        try:
            a = float(x)
        except (TypeError, ValueError):
            return False
        else:
            return True

    def _is_int(self, x):
        try:
            a = float(x)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            return a == b

    def _is_numeric(self, string):
        result = True
        try:
            x = float(string)
            result = (x == x) and (x - 1 != x)
        except ValueError:
            result = False
        return result

    def parse_uniforms(self, key, value):
        """
        Check uniforms that are added to ensure they conform to the correct type.

        If no uniform type is selected it will try to infer the type.

        :param key: uniform name
        :type key: str

        :param key: Comma seperated string
        :type key: str

        :return: uniform type and value for it
        :rtype: dict
        """
        if len(key) == 0 or len(value) == 0:
            return None

        data_type = ""
        uniforms_list = value.split(",")
        for uniform in uniforms_list:
            if not self._is_numeric(uniform):
                return None

        if not any([self._is_float(x) for x in uniforms_list]):
            data_type = "i"
            uniforms = [int(x) for x in uniforms_list]
        else:
            uniforms = [float(x) for x in uniforms_list]
            data_type = "f"

        uniform_type = "glUniform" + str(len(uniforms_list)) + data_type

        return {"type": uniform_type, "value": uniforms}
