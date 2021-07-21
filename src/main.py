import os
import sys

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
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.graphics import opengl

import numpy as np
from shader import Shader


sys.path.insert(1, os.getcwd()+'/bin')

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
		self.program = Shader("../resources/shaders/default.vert", "../resources/shaders/default.frag").get_program()

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
		#opengl.glDepthMask(opengl.GL_FALSE)
		opengl.glDepthFunc(opengl.GL_LESS)
		opengl.glEnable(opengl.GL_DEPTH_TEST)
		opengl.glClearColor(0.5, 0.5, 0.5,1.0)
		opengl.glClear(opengl.GL_COLOR_BUFFER_BIT | opengl.GL_DEPTH_BUFFER_BIT)

		#opengl.glDisable(opengl.GL_DEPTH_TEST)


class MainApp(App):
	cwd = os.getcwd()
	os.chdir(cwd)


	def onButtonPress(self, button):
		#self.app.reload_shaders()
		print("BUTTON PRESS")

	def OnSliderValueChange(self, instance, value):
		#self.app.change_scale(value)
		print(f"{instance}, {value}")

	def build(self):
		self.app = Application()
		#root = GridLayout(cols=1, padding=10)
		root = BoxLayout(orientation='vertical')
		#self.button = Button(text="Click for pop-up")
		#root.add_widget(self.button)

		tv = TreeView(root_options=dict(text='Solar System'),
					  hide_root=False,
					  indent_level=4)
		n1 = tv.add_node(TreeViewLabel(text="earth".capitalize()))
		n2 = tv.add_node(TreeViewLabel(text="mars".capitalize()))
		#for sub_object in self.app.solar_system.mars.planet['moons']:
		#	tv.add_node(TreeViewLabel(text=sub_object['name'].capitalize()), n2)
		#for sub_object in self.app.solar_system.earth.planet['moons']:
		#	tv.add_node(TreeViewLabel(text=sub_object['name'].capitalize()), n1)

		layout      = GridLayout(cols=1, padding=10)
		#popupLabel  = Label(text  = "Click for pop-up")
		scale_slider = Slider(min=-0, max=100, value=1)
		scale_slider.bind(value=self.OnSliderValueChange)
		closeButton = Button(text = "Reload\nShaders", size=(200, 50), on_press=self.onButtonPress)
		#layout.add_widget(Slider(value_track=True, value_track_color=[1, 0, 0, 1]))
		layout.add_widget(tv)
		layout.add_widget(scale_slider)
		layout.add_widget(closeButton)
		popup = Popup(title='Demo Popup',size_hint=(None, None), size=(200, 400), pos_hint={'top':.97,'right':.97},
					  content=layout, auto_dismiss=False)
		popup.open()  

		layout2 = BoxLayout(opacity=0.5)
		#pb = ProgressBar(max=1000, size=(100, 100))
		#pb.value = 750
		#layout2.add_widget(pb)
		#layout2.add_widget(Slider(value_track=True, value_track_color=[1, 0, 0, 1], size=(100, 100)))
		#layout2.add_widget(Button(text='Test Button', size=(100, 100)))

		# Draw the scene
		layout2.add_widget(self.app)
		root.add_widget(layout2)

		return root


if __name__ == "__main__":
	MainApp().run()