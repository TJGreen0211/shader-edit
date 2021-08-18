import json

import imgui
from array import array

from scene import Scene
import OpenGL.GL as opengl
import numpy as np
from PIL import Image

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from dialogs import FileChooser
from utility import textures
from gui_helper import GUIHelper


class GUI(Scene):
	def __init__(self):
		super().__init__()
		self.font = self.setup_font(
			"resources/fonts/"+self.config_dict["font"])
		self.color = tuple(self.config_dict['background_color'])
		self.current_object = 0
		self.vertex_shader = self.config_dict['shader_vs']
		self.fragment_shader = self.config_dict['shader_fs']

		self.object_map = ["Cube", "Sphere", "Torus", "Quad", "Triangle"]
		self.enable_blend = False
		self.enable_cull_face = False

		self.fps_values = array('f', [0 for x in range(100)])

		self.gui_helper = GUIHelper()

		self.shader_errors_list = []

		self.uniform_dict = {}

		self.uniform_name = ""
		self.uniform_value = ""
		self.uniform_parse_error = ""
		self.uniform_list_value = 0
		self.uniform_list = ["auto",
			"glUniform1f", "glUniform2f", "glUniform3f",
			"glUniform4f", "glUniform1i", "glUniform2i",
			"glUniform3i", "glUniform4i", "glUniform1ui",
			"glUniform2ui", "glUniform3ui", "glUniform4ui",
			"glUniform1fv", "glUniform2fv", "glUniform3fv",
			"glUniform4fv", "glUniform1iv", "glUniform2iv",
			"glUniform3iv", "glUniform4iv", "glUniform1uiv",
			"glUniform2uiv", "glUniform3uiv", "glUniform4uiv",
			"glUniformMatrix2fv", "glUniformMatrix3fv", "glUniformMatrix4fv",
			"glUniformMatrix2x3fv", "glUniformMatrix3x2fv", "glUniformMatrix2x4fv",
			"glUniformMatrix4x2fv", "glUniformMatrix3x4fv", "glUniformMatrix4x3fv"]

		self.textures_list = []
		self.mouse_reset_down = True
		self.add_image_button_texture = textures.Textures("resources/images/plus.png")


	def reset_state(self):
		self.color = tuple(self.config_dict['background_color'])
		self.uniform_dict = {}
		self.vertex_shader = self.config_dict['shader_vs']
		self.fragment_shader = self.config_dict['shader_fs']
		self.config_dict['current_object'] = 0
		self.load_object(self.config_dict['current_object'])
		self.reload_shaders(self.vertex_shader, self.fragment_shader)


	def load_save_state(self, save_dict):
		self.color = tuple(save_dict['background_color'])
		self.uniform_dict = save_dict['uniforms']
		self.vertex_shader = save_dict['shader_vs']
		self.fragment_shader = save_dict['shader_fs']
		self.config_dict['current_object'] = save_dict['current_object']
		self.textures_list = []
		for tex in save_dict['textures']:
			self.textures_list.append(textures.Textures(tex))
		self.load_object(self.config_dict['current_object'])
		self.reload_shaders(self.vertex_shader, self.fragment_shader)


	def save_state(self):
		save_dict = {}
		save_dict['background_color'] = list(self.color)
		save_dict['uniforms'] = self.uniform_dict
		save_dict['shader_vs'] = self.vertex_shader
		save_dict['shader_fs'] = self.fragment_shader
		save_dict['current_object'] = self.config_dict['current_object']
		save_dict['textures'] = [x.path for x in self.textures_list]
		FileChooser().save_file_dialog(save_dict)
		while Gtk.events_pending():
  			Gtk.main_iteration()

	def save_fbo_as_image(self):
		pixels = opengl.glReadPixels(0, 0, self.window_width, self.window_height, opengl.GL_RGBA, opengl.GL_UNSIGNED_BYTE)
		#array = np.array(pixels, dtype=np.ubyte)
		#data = glReadPixels (0, 0, image.width, image.height, GL_RGB,  GL_UNSIGNED_BYTE)
		image = Image.new ("RGB", (self.window_width, self.window_height), (0, 0, 0))
		image.frombytes (pixels)
		image = image.transpose(Image.FLIP_TOP_BOTTOM)
		image.save ('result.jpg')


		# Use PIL to create an image from the new array of pixels
		#new_image = Image.fromarray(array)
		#new_image.save('new.png')


	def menu(self):
		with imgui.font(self.font):
			imgui.begin("Menu")
			if imgui.begin_main_menu_bar():
				# first menu dropdown
				if imgui.begin_menu('File', True):
					if(imgui.menu_item('Save', 'Ctrl+S', False, True)[0]):
						self.save_state()

					if(imgui.menu_item('Open ...', 'Ctrl+O', False, True)[0]):
						file_path = FileChooser().open_file_dialog(start_directory='resources/saves')
						while Gtk.events_pending():
  							Gtk.main_iteration()
						try:
							with open(file_path, 'r') as f:
								self.load_save_state(json.load(f))
						except:
							pass
							
					if(imgui.menu_item('New', 'Ctrl+N', False, True)[0]):
						self.reset_state()
					

					if(imgui.menu_item('Import Object ...', 'Ctrl+I', False, True)[0]):
						object_path = FileChooser().open_file_dialog(start_directory='resources/objects')
						while Gtk.events_pending ():
  							Gtk.main_iteration()
						if object_path != "":
							self.load_object(0, object_path)


					if(imgui.menu_item('Quit ...', 'Ctrl+Q', False, True)[0]):
						self.close_window()

					imgui.end_menu()

				if imgui.begin_menu('Shaders', True):
					if(imgui.menu_item('Open ...', 'Ctrl+O', False, True)[0]):
						shader_paths = FileChooser().open_multiple_file_dialog()
						while Gtk.events_pending ():
  							Gtk.main_iteration()
						for shader_path in shader_paths:
							if shader_path.split(".")[-1] == "vert":
								self.vertex_shader = shader_path
							else:
								self.fragment_shader = shader_path
								
						self.reload_shaders(self.vertex_shader, self.fragment_shader)

					imgui.end_menu()

				imgui.end_main_menu_bar()
				

			if(imgui.button("Reload Shaders")):
				self.shader_errors_list = self.reload_shaders(self.vertex_shader, self.fragment_shader)

			color_changed, self.color = imgui.color_edit4(
				"Background Color", *self.color, show_alpha=True)
			if(color_changed):
				self.config_dict['background_color'] = [*self.color]

			imgui.plot_lines("", self.fps_values, scale_min=0.0, overlay_text="FPS: " +
							 str(self.fps_values[-1]), graph_size=(300.0, 50.0))

			combo_clicked, self.config_dict['current_object'] = imgui.combo(
				"combo", self.config_dict['current_object'], self.object_map
			)
			if(combo_clicked):
				self.load_object(self.config_dict['current_object'])

			imgui.text('\nUniforms:')
			changed, self.uniform_name = imgui.input_text(
				'Name',
				self.uniform_name,
				256
			)
			changed, self.uniform_value = imgui.input_text(
				'Value',
				self.uniform_value,
				256
			)
			combo_clicked, self.uniform_list_value = imgui.combo(
				"Type", self.uniform_list_value, self.uniform_list
			)

			if(imgui.button("Add Uniform")):
				new_uniform = self.gui_helper.parse_uniforms(
					self.uniform_name, self.uniform_value)
				if new_uniform is not None:
					self.uniform_dict[self.uniform_name] = new_uniform
					self.uniform_name = ""
					self.uniform_value = ""
				else:
					self.uniform_parse_error = "error parsing uniform"
			imgui.same_line()
			imgui.text(self.uniform_parse_error)
			#print(imgui.get_io().mouse_down[1])

			
			selected = [False for x in range(len(self.uniform_dict.keys()))]

			selectable_index = 0
			for key, value in self.uniform_dict.copy().items():
				_, selected[selectable_index] = imgui.selectable(
					f"{key}: {value['type'] + '['+str(value['value'])[1:-1] +']'}", selected[selectable_index]
				)
				if imgui.core.is_item_hovered():
					if imgui.get_io().mouse_down[1] and self.mouse_reset_down:
						self.mouse_reset_down = False
						del self.uniform_dict[key]
					#if imgui.get_io().mouse_down[0]:
					if selected[selectable_index]:
						self.uniform_name = key
						self.uniform_value = "".join(str(value['value'])[1:-1])	

				if not imgui.get_io().mouse_down[1]:
					self.mouse_reset_down = True

				selectable_index += 1

			imgui.begin_child("region", 450, 200, border=True)
			imgui.core.push_text_wrap_position(wrap_pos_x=0.0)
			imgui.text("Errors:")

			if len(self.shader_errors_list) > 0:
				for error in self.shader_errors_list:
					imgui.text(error)
			imgui.core.pop_text_wrap_position()
			imgui.end_child()
			
			total_texture_width = 128
			for texture in self.textures_list:
				imgui.image(texture.icon_id, texture.icon_width, texture.icon_height, border_color=(1, 0, 0, 1))
				total_texture_width += texture.icon_width
				if imgui.core.get_window_content_region_width() > total_texture_width:
					imgui.same_line()

			
			if(imgui.core.image_button(
				self.add_image_button_texture.icon_id, 
				self.add_image_button_texture.icon_width, 
				self.add_image_button_texture.icon_height, 
				border_color=(1, 0, 0, 0)
			)):
				image_path = FileChooser().open_file_dialog(start_directory='resources/images')
				while Gtk.events_pending ():
  					Gtk.main_iteration()
				self.textures_list.append(textures.Textures(image_path))
				

			_, self.enable_blend = imgui.checkbox("Enable Blending", self.enable_blend)
			_, self.enable_cull_face = imgui.checkbox("Enable Face Culling", self.enable_cull_face)

			#if(imgui.button("Save Image")):
			#	self.save_fbo_as_image()
			imgui.end()

	def start_imgui_frame(self):
		self.impl.process_inputs()
		imgui.new_frame()

	def render_imgui(self):
		imgui.render()
		self.impl.render(imgui.get_draw_data())

	def shutdown_imgui(self):
		self.impl.shutdown()

	def setup_font(self, font):
		io = imgui.get_io()
		new_font = io.fonts.add_font_from_file_ttf(font, 20)
		self.impl.refresh_font_texture()
		return new_font
