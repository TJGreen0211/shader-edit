import os
import json

import imgui

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
        f = filedialog.asksaveasfile(mode='w', defaultextension=".json", initialdir=os.path.join(
            os.getcwd(), self.save_file_path))
        if f is None:
            return
        json.dump(save_dict, f)
        f.close()

    def workspace_open(self):
        file_path = filedialog.askopenfilename(
            parent=self.root, title='Open Workspace', initialdir=os.path.join(os.getcwd(), self.save_file_path))
        # Opening JSON file
        f = open(file_path, 'r')
        data = json.load(f)
        f.close()
        return data


class GUI(Scene):
    def __init__(self):
        super().__init__()

        self.font = self.setup_font(
            "resources/fonts/"+self.config_dict["font"])
        self.color = tuple(self.config_dict['background_color'])

        self.object_map = ["Cube", "Sphere", "Quad", "Triangle"]

        self.fps_values = array('f', [0 for x in range(100)])

        self.shader_errors_list = []

        self.uniform_dict = {
            "one": {
                "type": "glUniform3f",
                "value": [1.0, 0.0, 0.0]
            },
            "two": {
                "type": "glUniform1f",
                "value": [0.0]
            },
            "three": {
                "type": "glUniform2f",
                "value": [1.0, 0.0]
            }
        }

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

    def parse_uniforms(self, key, value):

        if len(key) == 0 or len(value) == 0:
            return None
        return {"type": "gluniform3f", "value": value}

    def menu(self):
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
                        # print(self.config_dict)

                    #imgui.menu_item('New', 'Ctrl+N', False, True)

                    # submenu
                    if imgui.begin_menu('Import Object', True):
                        imgui.menu_item('doc.txt', None, False, True)
                        imgui.end_menu()

                    if(imgui.menu_item('Quit ...', 'Ctrl+Q', False, True)[0]):
                        self.close_window()

                    imgui.end_menu()

                imgui.end_main_menu_bar()

            if(imgui.button("Reload Shaders")):
                self.shader_errors_list = self.reload_shaders()

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

            # TODO: Decide if I want this
            # _, self.rotatation_speed = imgui.slider_float(
            #	"Spin", self.rotatation_speed,
            #	min_value=0.0, max_value=100.0,
            #	format="%.1f",
            #	power=1.0
            # )

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
                new_uniform = self.parse_uniforms(
                    self.uniform_name, self.uniform_value)
                if new_uniform is not None:
                    self.uniform_dict[self.uniform_name] = new_uniform
                    self.uniform_name = ""
                    self.uniform_value = ""
                else:
                    self.uniform_parse_error = "error parsing uniform"
            imgui.same_line()
            imgui.text(self.uniform_parse_error)

            uniforms = [x.strip() for x in self.uniform_name.split(",")]
            for key, value in self.uniform_dict.items():
                imgui.text(
                    f"{key}: {value['type'] + '['+str(value['value'])[1:-1] +']'}")

            imgui.begin_child("region", 450, -50, border=True)
            imgui.core.push_text_wrap_position(wrap_pos_x=0.0)
            imgui.text("Errors:")

            if len(self.shader_errors_list) > 0:
                for error in self.shader_errors_list:
                    imgui.text(error)
            imgui.core.pop_text_wrap_position()
            imgui.end_child()

            # _, self.zoom = imgui.slider_float(
            #    "slide floats", self.zoom,
            #    min_value=0.0, max_value=100.0,
            #    format="%.1f",
            #    power=1.0
            # )

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
