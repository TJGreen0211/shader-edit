
import os
import json

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class FileChooser():
	def __init__(self):
		self.w = Gtk.Window ()

	def open_multiple_file_dialog(self):
		dia = Gtk.FileChooserDialog("Please Choose Shader Files", self.w,
			Gtk.FileChooserAction.OPEN, (
				Gtk.STOCK_CANCEL, 
				Gtk.ResponseType.CANCEL,
			 	Gtk.STOCK_OPEN, 
				Gtk.ResponseType.OK
				)
			)
		Gtk.FileChooser.set_select_multiple(dia, True)
		Gtk.FileChooser.set_current_folder(dia, os.path.join(os.getcwd(), 'resources/shaders'))

		paths = []

		self.add_filters(dia)
		response = dia.run()
		if response == Gtk.ResponseType.OK:
			paths = dia.get_filenames()
		elif response == Gtk.ResponseType.CANCEL:
			pass
			#print("Cancel clicked")
		
		dia.destroy()

		return paths
		
	def open_file_dialog(self, start_directory="resources"):
		dia = Gtk.FileChooserDialog("Please choose a file", self.w,
			Gtk.FileChooserAction.OPEN, (
				Gtk.STOCK_CANCEL, 
				Gtk.ResponseType.CANCEL,
			 	Gtk.STOCK_OPEN, 
				Gtk.ResponseType.OK
				)
			)
		Gtk.FileChooser.set_current_folder(dia, os.path.join(os.getcwd(), start_directory))

		path = ''

		self.add_filters(dia)
		response = dia.run()
		if response == Gtk.ResponseType.OK:
			path = dia.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			pass
			#print("Cancel clicked")
		
		dia.destroy()

		return path

	def save_file_dialog(self, save_dict):
		dia = Gtk.FileChooserDialog("Please choose a file", self.w,
			Gtk.FileChooserAction.SAVE, (
				Gtk.STOCK_CANCEL, 
				Gtk.ResponseType.CANCEL,
			 	Gtk.STOCK_SAVE, 
				Gtk.ResponseType.OK
				)
			)
		Gtk.FileChooser.set_current_folder(dia, os.path.join(os.getcwd(), 'resources/saves'))
		self.add_filters(dia)
		response = dia.run()

		file_path = ''
		if response == Gtk.ResponseType.OK:
			file_path = dia.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			pass
			#print("Cancel clicked")

		if file_path != '':
			try:
				with open(file_path, 'w') as f:
					json.dump(save_dict, f, indent=4)
			except:
				pass

		dia.destroy()
	
	def add_filters(self, dia):
		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dia.add_filter(filter_any)

	def get_path(self):
		return self.path
