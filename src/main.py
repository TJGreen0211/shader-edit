import os
import sys
import math
import ctypes

import kivy
kivy.require('1.1.1')
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.resources import resource_find
#from kivy.graphics.transformation import Matrix
from kivy.graphics import Fbo
from kivy.graphics import Rectangle

from kivy.graphics import opengl

import numpy as np

sys.path.insert(1, os.getcwd()+'/bin')

vertex_code = b"""
	uniform mat4 u_projection_mat;
	attribute vec3 a_position;
	varying vec4 v_color;
	void main()
	{
		gl_Position = u_projection_mat*vec4(a_position, 1.0);
		v_color = (vec4(a_position, 1.0)+1.0)/2.0;
	} """



fragment_code = b"""
	varying vec4 v_color;
	void main()
	{
		gl_FragColor = v_color;
	} """


#def createShader(vertPath, fragPath, tchsPath=None, teshPath=None, geomPath=None):
#	vert = loadShaderString(vertPath)
#	vertId = loadShader(vert, GL_VERTEX_SHADER)
#
#	frag = loadShaderString(fragPath)
#	fragId = loadShader(frag, GL_FRAGMENT_SHADER)
#
#	return LinkShader(fragID, vertID)


data = np.array([ -0.5,-0.5,0.5,
					0.5,-0.5,0.5,
					0.5,0.5,0.5,
				   -0.5,0.5,0.5], dtype=np.float32)



index = np.array([0,1,2,  2,3,0],dtype=np.uint32)


class Application(Widget):
	def __init__(self, **kwargs):
		super(Application, self).__init__(**kwargs)
		self.angle=0
		self.setup_kvfbo()
		self.setup_glfbo()

		Clock.schedule_interval(self.update_glsl, 1.0 / 60.0)

	def update_glsl(self, *largs):
		self.angle+=0.01
		if 0:
			self.draw_fbo(self.kvfboid)
		else:
			self.draw_fbo(self.glfboid)
			self.blit_fbo()
		self.canvas.ask_update()

	def setup_kvfbo(self):
		self.kvfbo = Fbo(with_depthbuffer = True, size = Window.size, compute_normal_mat=True)
		self.canvas.add(self.kvfbo)
		self.canvas.add(Rectangle(size=Window.size, texture=self.kvfbo.texture))
		self.kvfbo.bind()
		(self.kvfboid,)=opengl.glGetIntegerv(opengl.GL_FRAMEBUFFER_BINDING)
		self.kvfbo.release()

	def setup_glfbo(self):
		self.program = opengl.glCreateProgram()

		vertex	 = opengl.glCreateShader(opengl.GL_VERTEX_SHADER)
		fragment = opengl.glCreateShader(opengl.GL_FRAGMENT_SHADER)
		opengl.glShaderSource(vertex, vertex_code)
		opengl.glShaderSource(fragment, fragment_code)
		opengl.glCompileShader(vertex)
		opengl.glCompileShader(fragment)

		opengl.glAttachShader(self.program, vertex)
		opengl.glAttachShader(self.program, fragment)
		opengl.glLinkProgram(self.program)
		opengl.glDetachShader(self.program, vertex)
		opengl.glDetachShader(self.program, fragment)
		opengl.glUseProgram(self.program)

		self.w, self.h = Window.width, Window.height
		opengl.glEnable(opengl.GL_TEXTURE_2D)
		(self.glfboid,) = opengl.glGenFramebuffers(1)
		(self.gltexid,) = opengl.glGenTextures(1)
		opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER, self.glfboid)
		opengl.glBindTexture(opengl.GL_TEXTURE_2D, self.gltexid)

		opengl.glTexImage2D(opengl.GL_TEXTURE_2D, 0, opengl.GL_RGBA, self.w, self.h, 0, opengl.GL_RGBA, opengl.GL_UNSIGNED_BYTE, (np.ones(self.w*self.h*4, np.uint8)*128).tobytes())
		opengl.glFramebufferTexture2D(opengl.GL_FRAMEBUFFER, opengl.GL_COLOR_ATTACHMENT0, opengl.GL_TEXTURE_2D,self.gltexid,0)
		opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER, 0)
		opengl.glBindTexture(opengl.GL_TEXTURE_2D, 0)

		(self.vbo,) = opengl.glGenBuffers(1)
		opengl.glBindBuffer(opengl.GL_ARRAY_BUFFER, self.vbo)
		opengl.glBufferData(opengl.GL_ARRAY_BUFFER, data.nbytes, data.tobytes(), opengl.GL_DYNAMIC_DRAW)
		(self.ibo,)= opengl.glGenBuffers(1)
		opengl.glBindBuffer(opengl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)
		opengl.glBufferData(opengl.GL_ELEMENT_ARRAY_BUFFER, index.nbytes, index.tobytes(), opengl.GL_STATIC_DRAW)


	def blit_fbo(self):
		opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER, self.glfboid)
		pixels = opengl.glReadPixels(0, 0, self.w, self.h, opengl.GL_RGBA, opengl.GL_UNSIGNED_BYTE)
		opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER,self.kvfboid)
		opengl.glTexSubImage2D(opengl.GL_TEXTURE_2D, 0 ,0, 0, self.w, self.h, opengl.GL_RGBA, opengl.GL_UNSIGNED_BYTE, pixels)
		opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER,0)


	def draw_fbo(self, targetfbo):
		eye=np.matrix([[np.cos(self.angle),-np.sin(self.angle),0,0],
				[np.sin(self.angle),np.cos(self.angle),0,0],
				[0,0,1,0],
				[0,0,0,1]],dtype=np.float32)

		opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER,targetfbo)
		opengl.glClear(opengl.GL_COLOR_BUFFER_BIT)

		opengl.glBindBuffer(opengl.GL_ARRAY_BUFFER, self.vbo)
		opengl.glBindBuffer(opengl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

		opengl.glUseProgram(self.program)
		u_loc = opengl.glGetUniformLocation(self.program, b"u_projection_mat")
		opengl.glUniformMatrix4fv(u_loc, 1, False, np.array(eye).flatten().tobytes() )
		a_loc = opengl.glGetAttribLocation(self.program, b"a_position")
		opengl.glEnableVertexAttribArray(a_loc)
		opengl.glVertexAttribPointer(a_loc, 3, opengl.GL_FLOAT, False, 12, 0)

		opengl.glViewport(0,0,self.w,self.h)
		opengl.glDrawElements(opengl.GL_TRIANGLES, 6, opengl.GL_UNSIGNED_INT, 0)
		opengl.glBindFramebuffer(opengl.GL_FRAMEBUFFER, 0)


	def update(self, dt):
		#glViewport(0, 0, width, height)
		opengl.glEnable(opengl.GL_DEPTH_TEST)
		opengl.glClearColor(0.5, 0.5, 0.5,1.0)
		opengl.glClear(opengl.GL_COLOR_BUFFER_BIT | opengl.GL_DEPTH_BUFFER_BIT)


class MainApp(App):
	cwd = os.getcwd()
	os.chdir(cwd)

	def build(self):
		#application = ApplicationRun()
		#Clock.schedule_interval(application.update, 1.0 / 60.0)
		return Application()


if __name__ == "__main__":
	MainApp().run()