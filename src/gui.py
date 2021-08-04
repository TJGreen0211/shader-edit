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
		
		#self.window = window
		self.impl = GlfwRenderer(self.window, attach_callbacks=False)

		#self.impl.keyboard_callback

		self.font = self.setup_font("resources/fonts/"+self.config_dict["font"])
		self.color = tuple(self.config_dict['background_color'])

		self.object_map = ["Cube", "Sphere", "Quad", "Triangle"]

		self.fps_values = array('f', [0 for x in range(100)])
		

	def menu(self):

		#io = imgui.get_io()
		#print(io.mouse_wheel)
		
		with imgui.font(self.font):
			if imgui.begin_main_menu_bar():
				# first menu dropdown
				if imgui.begin_menu('File', True):
					if(imgui.menu_item('Save', 'Ctrl+S', False, True)[0]):
						WorkspaceMenu().workspace_save(self.config_dict)
					
					if(imgui.menu_item('Open ...', 'Ctrl+O', False, True)[0]):
						loaded_dict = WorkspaceMenu().workspace_open()
						for key, value in loaded_dict.items():
							self.config_dict[key] = loaded_dict[key]
						
						#self.color = tuple(self.config_dict['background_color'])
						#print(self.config_dict)

					imgui.menu_item('New', 'Ctrl+N', False, True)
			
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
			color_changed, self.color = imgui.color_edit4("Background Color", *self.color, show_alpha=True)
			if(color_changed):
				self.config_dict['background_color'] = [*self.color]

			imgui.plot_lines("", self.fps_values, scale_min=0.0, overlay_text="FPS: "+str(self.fps_values[-1]), graph_size=(300.0, 50.0))

			combo_clicked, self.config_dict['current_object'] = imgui.combo(
				"combo", self.config_dict['current_object'], self.object_map
			)
			if(combo_clicked):
				self.load_object(self.config_dict['current_object'])

			_, self.rotatation_speed = imgui.slider_float(
			    "slide floats", self.rotatation_speed,
			    min_value=0.0, max_value=100.0,
			    format="%.1f",
			    power=1.0
			)

			#_, self.zoom = imgui.slider_float(
			#    "slide floats", self.zoom,
			#    min_value=0.0, max_value=100.0,
			#    format="%.1f",
			#    power=1.0
			#)

			#print(imgui.core.get_scroll_y())


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
