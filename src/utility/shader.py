"""Common shader functions."""

import OpenGL.GL as opengl


class Shader(object):
    """Parse and load a shader file."""

    def __init__(self, *argv):
        """
        Create a shader object. Currently only supports Vertex and Fragment shaders.

        :param vert: Vertex shader path
        :type vert: str

        :param frag: Fragment shader path
        :type frag: str

        :return: Shader object
        :rtype: obj
        """
        self.program = opengl.glCreateProgram()
        self.shader_error = []

        shader_ids = []
        for shader_path in argv:
            shader_ids.append(self._compile_shader(shader_path))

        for shader in shader_ids:
            opengl.glAttachShader(self.program, shader)

        opengl.glLinkProgram(self.program)

        for shader in shader_ids:
            opengl.glDetachShader(self.program, shader)

    def _compile_shader(self, path):
        extension_map = {
            "vert": opengl.GL_VERTEX_SHADER,
            "frag": opengl.GL_FRAGMENT_SHADER,
        }
        return self._create_shader(path, extension_map[path.split('.')[-1]])

    def _create_shader(self, path, shader_type):
        shader_code = self._read_shader(path)
        shader = opengl.glCreateShader(shader_type)
        opengl.glShaderSource(shader, shader_code)
        opengl.glCompileShader(shader)
        self._check_err(shader, path.split("/")[-1])
        # self.link_shader(shader)

        return shader

    def link_shader(self, shader):
        """TODO"""
        opengl.glAttachShader(self.program, shader)
        opengl.glLinkProgram(self.program)
        opengl.glDetachShader(self.program, shader)

    def _read_shader(self, path):
        with open(path, 'r') as f:
            return f.read().encode()

    def _check_err(self, shader, name):
        err = opengl.glGetShaderiv(shader, opengl.GL_COMPILE_STATUS)
        if err != opengl.GL_TRUE:
            self.shader_error.append(
                f"Error in {name}: {opengl.glGetShaderInfoLog(shader).decode('ASCII')}")

    def get_program(self):
        """
        Get the shader program.

        :return: Shader program
        :rtype: obj
        """
        return self.program
