import os
import json

import imgui
from imgui.integrations.glfw import GlfwRenderer

import tkinter as tk
from tkinter import filedialog
from array import array

from scene import Scene


class WorkspaceMenu(object):
	def __init__(self):
		self.root = tk.Tk()
		self.root.withdraw()
		self.save_file_path = "resources/saves"

	def workspace_save(self, save_dict):
		f = filedialog.asksaveasfile(mode='w', defaultextension=".json", initialdir=os.path.join(os.getcwd(), self.save_file_path))
		if f is None: 
			return
		json.dump(save_dict, f)
		f.close()

	def workspace_open(self):
		file_path = filedialog.askopenfilename(parent=self.root, title='Open Workspace', initialdir=os.path.join(os.getcwd(), self.save_file_path))
		# Opening JSON file
		f = open(file_path, 'r')
		data = json.load(f)
		f.close()
		return data


class GUI(Scene):
	def __init__(self):
		super().__init__()
		imgui.create_context()
		#self.window = window
		self.impl = GlfwRenderer(self.window)

		self.font = self.setup_font("resources/fonts/"+self.config_dict["font"])
		self.color = tuple(self.config_dict['background_color'])
		self.current = self.config_dict['current_object']

		self.object_map = ["Cube", "Sphere", "Quad", "Triangle"]

		self.value = 88.2

		self.fps_values = array('f', [0 for x in range(100)])
		

	def menu(self):
		
		with imgui.font(self.font):
			if imgui.begin_main_menu_bar():
				# first menu dropdown
				if imgui.begin_menu('File', True):
					#if(imgui.menu_item('Save', 'Ctrl+S', False, True)[0]):
					#	WorkspaceMenu().workspace_save(self.self.config_dict_dict)
					imgui.menu_item('New', 'Ctrl+N', False, True)
					imgui.menu_item('Open ...', 'Ctrl+O', False, True)
			
					# submenu
					if imgui.begin_menu('Open Recent', True):
						imgui.menu_item('doc.txt', None, False, True)
						imgui.end_menu()
			
					imgui.end_menu()
			
				imgui.end_main_menu_bar()

			if(imgui.button("Reload Shaders")):
				self.reload_shaders()
				#root = tk.Tk()
				#root.withdraw()
				#file_path = filedialog.askopenfilenames(parent=root, title='Choose shader files')
				#print(file_path)
			
			#bg_color = self.config_dict['background_color']
			_, self.color = imgui.color_edit4("Background Color", *self.color, show_alpha=True)

			imgui.plot_lines("FPS", self.fps_values)

			combo_clicked, self.current = imgui.combo(
				"combo", self.current, self.object_map
			)
			if(combo_clicked):
				self.config_dict['current_object'] = self.current
				self.load_object(self.current)

			_, self.rotatation_speed = imgui.slider_float(
			    "slide floats", self.rotatation_speed,
			    min_value=0.0, max_value=100.0,
			    format="%.1f",
			    power=1.0
			)


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
