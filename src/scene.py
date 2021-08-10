
import glfw

import numpy as np
import imgui
import time

from imgui.integrations.glfw import GlfwRenderer
from OpenGL.GL import *
from numpy.core.numeric import indices
from numpy.lib.function_base import append

from shader import Shader
import matmath
import obj
from camera import Camera


class Scene(GlfwRenderer):
	def __init__(self):
		self.window_width = 1280
		self.window_height = 720
		self.window = self.create_window()
		imgui.create_context()
		self.impl = GlfwRenderer(self.window, attach_callbacks=False)
		self.setup_glfw()
		self.rotatation_speed = 0.0
		self.zoom = -3.0
		self.before = time.time()

		self.config_dict = {
			"background_color": [0.0, 0.0, 0.0, 1.0],
			"shader_vs": "resources/shaders/default.vert",
			"shader_fs": "resources/shaders/default.frag",
			"current_object": 0,
			"window_width": 1280,
			"window_height": 720,
			"font": "DroidSans.ttf"
		}

		self.camera = Camera(mouse_scroll=-3.0)

		self.perspective = matmath.mat4_perspective(90.0, float(
			self.window_width)/float(self.window_height), 0.1, 5000.0)
		self.shader = Shader(
			self.config_dict["shader_vs"], self.config_dict["shader_fs"]).get_program()
		self.init_opengl()
		self.vao = self.load_object(0)

		self.model = np.identity(4, dtype=np.float32)

		self.model[0][3] = 0.0
		self.model[1][3] = 0.0
		self.model[2][3] = -3.0

	def reload_shaders(self, vert, frag):
		shader = Shader(
			vert, frag)
		if len(shader.shader_error) == 0:
			self.shader = shader.get_program()

		return shader.shader_error

	def close_window(self):
		glfw.set_window_should_close(self.window, True)

	def scroll_callback(self, window, x_offset, y_offset):
		self.camera.process_mouse_scroll(y_offset, 0.0)

	def mouse_callback(self, window, xpos, ypos):
		state = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT)
		#xpos = 1.0*xpos/getWindowWidth()*2 - 1.0;
		#ypos =  1.0*ypos/getWindowHeight()*2 - 1.0;
		if state == glfw.PRESS:
			self.camera.process_mouse_movement(xpos, ypos, False)
			# processMouseMovement(&camera, xpos, ypos, 0, delta_time)
		else:
			self.camera.process_mouse_movement(xpos, ypos, True)
			# processMouseMovement(&camera, xpos, ypos, 1, delta_time)

	def framebuffer_size_callback(self, window, width, height):
		# make sure the viewport matches the new window dimensions; note that width and
		# height will be significantly larger than specified on retina displays.
		# camera.perspective_matrix = mat4Perspective(90.0, (float)width/(float)height, 0.1, 5000.0);
		# framebuffer_init((float)width, (float)height, &scene_frambuffer);
		#print("Framebuffer: %d, %d\n", width, height);
		self.window_width = width
		self.window_height = height
		self.perspective = matmath.mat4_perspective(90.0, float(
			self.window_width)/float(self.window_height), 0.1, 5000.0)
		glViewport(0, 0, width, height)

	def init_opengl(self):
		glViewport(0, 0, self.window_width, self.window_height)
		col = tuple(self.config_dict['background_color'])
		glClearColor(*col)

	def load_object(self, object_index, object_path=None):

		if object_path is not None:
			try:
				object_vertices = obj.object_load(object_path)
			except:
				object_vertices = []
		else:
			object_map = ["Cube", "Sphere", "Quad", "Triangle"]
			if object_map[object_index] == "Quad":
				object_vertices = [
					-1.0,  1.0, 0.0,
					-1.0, -1.0, 0.0,
					1.0, -1.0, 0.0,
					-1.0,  1.0, 0.0,
					1.0, -1.0, 0.0,
					1.0,  1.0, 0.0]
			elif object_map[object_index] == "Triangle":
				object_vertices = [-0.5, -0.5, 0.0,
								   0.5, -0.5, 0.0,
								   0.0, 0.5, 0.0]
			else:
				object_vertices = obj.object_load(
					"resources/objects/"+object_map[object_index].lower()+".obj")
		

		object_vertices = np.array(object_vertices, dtype=np.float32)
		self.n_vertices = int(len(object_vertices)/3)
		# print(object_vertices.nbytes)

		vao = glGenVertexArrays(1)
		VBO = glGenBuffers(1)
		glBindVertexArray(vao)

		# Bind the buffer
		glBindBuffer(GL_ARRAY_BUFFER, VBO)
		glBufferData(GL_ARRAY_BUFFER, object_vertices.nbytes,
					 object_vertices, GL_STATIC_DRAW)

		# get the position from vertex shader
		#position = glGetAttribLocation(self.shader, 'position')
		glEnableVertexAttribArray(0)
		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
		

		glEnableVertexAttribArray(0)
		glBindVertexArray(0)

		self.vao = vao

		return self.vao

	def get_delta_time(self, last_frame):
		current_frame = glfw.get_time()
		delta_time = current_frame - last_frame
		last_frame = current_frame
		return delta_time

	def mouse_button_callback(self, window, button, action, mods):
		if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.RELEASE:
			now = time.time()
			diff_ms = (now - self.before)*100.0
			self.before = now
			if diff_ms > 1 and diff_ms < 20:
				self.camera.reset_view()

	def create_window(self):
		# GLFW initialization
		if not glfw.init():
			return

		mode = glfw.get_video_mode(glfw.get_primary_monitor())
		window = glfw.create_window(
			self.window_width, self.window_height, "Shader Edit", None, None)
		if not window:
			glfw.terminate()
			return
		glfw.make_context_current(window)

		return window

	def setup_glfw(self):
		glfw.set_framebuffer_size_callback(
			self.window, self.framebuffer_size_callback)

		# Need this for text input to work properly
		glfw.set_key_callback(self.window, self.impl.keyboard_callback)
		glfw.set_char_callback(self.window, self.impl.char_callback)

		# Override the default callbacks
		glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
		glfw.set_scroll_callback(self.window, self.scroll_callback)
		glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)

	def draw_object(self, uniform_dict):
		try:

			glUseProgram(self.shader)
			glBindVertexArray(self.vao)

			self.model = np.identity(4, dtype=np.float32)

			self.model[0][3] = 0.0
			self.model[1][3] = 0.0
			self.model[2][3] = self.camera.mouse_scroll


			for key, value in uniform_dict.items():
				# This is unsafe but I don't care
				eval(value['type'])(glGetUniformLocation(self.shader, bytes(key, 'utf-8')), *tuple(value['value']))

			glUniform3f(glGetUniformLocation(self.shader, b"camera_position"), *tuple(self.camera.get_camera_position(self.model)[0:3]))
			

			glUniformMatrix4fv(glGetUniformLocation(self.shader, b"model"), 1, False, self.model.flatten().tobytes())
			glUniformMatrix4fv(glGetUniformLocation(self.shader, b"view"), 1, False, self.camera.rotation_matrix.flatten().tobytes())
			u_loc = glGetUniformLocation(self.shader, b"projection")
			glUniformMatrix4fv(u_loc, 1, False, np.array(self.perspective).flatten().tobytes())
			glDrawArrays(GL_TRIANGLES, 0, self.n_vertices)
			glBindVertexArray(0)
		except Exception as e:
			print(e)
