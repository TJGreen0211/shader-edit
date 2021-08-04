
import glfw

import numpy as np
#from integration.glfw import GlfwRenderer
import imgui


from OpenGL.GL import *
from numpy.core.numeric import indices
from numpy.lib.function_base import append

from objloader import ObjFile
from shader import Shader
import matmath
import obj
from camera import Camera

class Scene(object):
	def __init__(self):
		self.window_width = 1280
		self.window_height = 720
		self.window = self.setup_glfw()
		imgui.create_context()
		#self.impl = super().__init__(self.window)
		self.rotatation_speed = 0.0
		self.zoom = 100.0


		self.config_dict = {
			"background_color": [0.0, 0.0, 0.0, 1.0],
			"shader_vs": "resources/shaders/default.vert",
			"shader_fs": "resources/shaders/default.frag",
			"current_object": 0,
			"window_width": 1280,
			"window_height": 720,
			"font": "DroidSans.ttf"
		}

		
		self.perspective = matmath.mat4_perspective(90.0, float(self.window_width)/float(self.window_height), 0.1, 5000.0)
		self.shader = Shader(self.config_dict["shader_vs"], self.config_dict["shader_fs"]).get_program()
		self.init_opengl()
		self.vao = self.init_objects()

		#self.gui = GUI(self.window, self.config_dict)

		self.model = np.identity(4, dtype=np.float32)

		self.model[0][3] = 0.0
		self.model[1][3] = 0.0
		self.model[2][3] = -3.0

		#self.setup_scene()

	def do_something(self):
		print("Testing")
		return super(Scene, self).do_something()

	def mouse_callback(self, *args, **kwargs):
		print("ASDFQUERTY")
		return super(Scene, self).mouse_callback(*args, **kwargs)

	def reload_shaders(self):
		self.shader = Shader(self.config_dict["shader_vs"], self.config_dict["shader_fs"]).get_program()

	def scroll_callback(self, window, x_offset, y_offset):
		print("ASDFQUERTY")
		self.zoom = Camera().process_mouse_scroll(y_offset, 0.0)

	#def mouse_callback( window, xpos, ypos):
	#	print(xpos)
	#	#int state = glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT)
	#	#xpos = 1.0*xpos/getWindowWidth()*2 - 1.0;
	#	#ypos =  1.0*ypos/getWindowHeight()*2 - 1.0;
	#	#if (state == GLFW_PRESS)
	#	#{
	#	#	processMouseMovement(&camera, xpos, ypos, 0, delta_time);
	#	#}
	#	#else {
	#	#	processMouseMovement(&camera, xpos, ypos, 1, delta_time);
	#	#}
#
	def framebuffer_size_callback(self, window, width, height):
		# make sure the viewport matches the new window dimensions; note that width and
		# height will be significantly larger than specified on retina displays.
		#camera.perspective_matrix = mat4Perspective(90.0, (float)width/(float)height, 0.1, 5000.0);
		#framebuffer_init((float)width, (float)height, &scene_frambuffer);
		#print("Framebuffer: %d, %d\n", width, height);
		self.window_width = width
		self.window_height = height
		self.perspective = matmath.mat4_perspective(90.0, float(self.window_width)/float(self.window_height), 0.1, 5000.0)
		glViewport(0, 0, width, height)

	def init_opengl(self):
		glViewport(0,0,self.window_width, self.window_height)
		col = tuple(self.config_dict['background_color'])
		glClearColor(*col)


	def init_objects(self):
		triangle = [-0.5,-0.5,0.0,
				 0.5,-0.5,0.0,
				 0.0,0.5, 0.0]

		#triangle = obj.object_load()
		triangle = np.array(triangle, dtype = np.float32)
		self.n_vertices = int(len(triangle)/3)
		print(triangle.nbytes)

		vao = glGenVertexArrays(1)
		VBO = glGenBuffers(1)
		glBindVertexArray(vao)

		#Bind the buffer
		glBindBuffer(GL_ARRAY_BUFFER, VBO)
		glBufferData(GL_ARRAY_BUFFER, triangle.nbytes, triangle, GL_STATIC_DRAW)
	
		#get the position from vertex shader
		position = glGetAttribLocation(self.shader, 'position')
		glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
		glEnableVertexAttribArray(position)

		glEnableVertexAttribArray(0)
		glBindVertexArray(0)

		return vao

	def load_object(self, object_index):

		object_map = ["Cube", "Sphere", "Quad", "Triangle"]
		object_vertices = obj.object_load("resources/objects/"+object_map[object_index].lower()+".obj")

		object_vertices = np.array(object_vertices, dtype = np.float32)
		self.n_vertices = int(len(object_vertices)/3)
		#print(object_vertices.nbytes)

		vao = glGenVertexArrays(1)
		VBO = glGenBuffers(1)
		glBindVertexArray(vao)

		#Bind the buffer
		glBindBuffer(GL_ARRAY_BUFFER, VBO)
		glBufferData(GL_ARRAY_BUFFER, object_vertices.nbytes, object_vertices, GL_STATIC_DRAW)
	
		#get the position from vertex shader
		position = glGetAttribLocation(self.shader, 'position')
		glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
		glEnableVertexAttribArray(position)

		glEnableVertexAttribArray(0)
		glBindVertexArray(0)

		self.vao = vao
		#print(m.vertices)

		#verts = []
		#for i in range(len(indices))
		#	verts.append()


	def setup_glfw(self):
		# GLFW initialization
		if not glfw.init():
			return

		mode = glfw.get_video_mode(glfw.get_primary_monitor())
		#window = glfw.create_window(mode.width, mode.height, "Shader Edit", None, None)
		window = glfw.create_window(self.window_width, self.window_height, "Shader Edit", None, None)
		if not window:
			glfw.terminate()
			return

		glfw.make_context_current(window)
		glfw.set_framebuffer_size_callback(window, self.framebuffer_size_callback)

		#glfw.set_key_callback(window, key_callback)
		glfw.set_cursor_pos_callback(window, self.mouse_callback)
		glfw.set_scroll_callback(window, self.scroll_callback)
		#glfw.set_mouse_button_callback(window, self.mouse_button_callback)

		return window

	def draw_object(self):
		#Draw Triangle
		glUseProgram(self.shader)
		glBindVertexArray(self.vao)

		glUniformMatrix4fv(glGetUniformLocation(self.shader, b"model"), 1, False, self.model.flatten().tobytes())
		u_loc = glGetUniformLocation(self.shader, b"projection")
		glUniformMatrix4fv(u_loc, 1, False, np.array(self.perspective).flatten().tobytes())
		glDrawArrays(GL_TRIANGLES, 0, self.n_vertices)
		glBindVertexArray(0)


	