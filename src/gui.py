import os
import json

import imgui
from imgui.integrations.glfw import GlfwRenderer

import tkinter as tk
from tkinter import filedialog
from array import array


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


class GUI(object):
	def __init__(self, window, config):
		imgui.create_context()
		self.window = window
		self.impl = GlfwRenderer(self.window)

		self.font = self.setup_font("resources/fonts/"+config["font"])
		self.color = tuple(config['background_color'])
		self.current = config['current_object']

		self.fps_values = array('f', [0 for x in range(100)])
		

	def menu(self, config):
		with imgui.font(self.font):
			if imgui.begin_main_menu_bar():
				# first menu dropdown
				if imgui.begin_menu('File', True):
					#if(imgui.menu_item('Save', 'Ctrl+S', False, True)[0]):
					#	WorkspaceMenu().workspace_save(self.config_dict)
					imgui.menu_item('New', 'Ctrl+N', False, True)
					imgui.menu_item('Open ...', 'Ctrl+O', False, True)
			
					# submenu
					if imgui.begin_menu('Open Recent', True):
						imgui.menu_item('doc.txt', None, False, True)
						imgui.end_menu()
			
					imgui.end_menu()
			
				imgui.end_main_menu_bar()

			if(imgui.button("Reload")):
				
				root = tk.Tk()
				root.withdraw()
				file_path = filedialog.askopenfilenames(parent=root, title='Choose shader files')
				print(file_path)
			
			#bg_color = config['background_color']
			_, self.color = imgui.color_edit4("Background Color", *self.color, show_alpha=True)

			imgui.plot_lines("FPS", self.fps_values)

			combo_clicked, self.current = imgui.combo(
				"combo", self.current, ["Sphere", "Cube", "Quad", "Triangle"]
			)
			if(combo_clicked):
				config['current_object'] = self.current

		return config


	def start_frame(self):
		self.impl.process_inputs()
		imgui.new_frame()

	def render(self):
		imgui.render()
		self.impl.render(imgui.get_draw_data())

	def shutdown(self):
		self.impl.shutdown()

	def setup_font(self, font):
		io = imgui.get_io()
		new_font = io.fonts.add_font_from_file_ttf(font, 20)
		self.impl.refresh_font_texture()
		return new_font
