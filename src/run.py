
import math
import glfw

from OpenGL.GL import *
from gui import GUI

import math
import numpy as np

#from scene import Scene


class App(GUI):
    def __init__(self):
        super().__init__()

    def run(self):
        frame_count = 0
        time_count = 0.0
        last_frame = 0.0

        #color = (0.1, 0.5, 0.7, 1.0)
        glDisable(GL_CULL_FACE)
        # glDisable(GL_DEPTH_TEST)
        glEnable(GL_DEPTH_TEST)

        self.view = np.identity(4, dtype=np.float32)

        while not glfw.window_should_close(self.window):

            frame_count += 1
            current_frame = glfw.get_time()
            if(current_frame - time_count >= 1.0):
                self.fps_values.pop(0)
                self.fps_values.append(frame_count)
                time_count = current_frame
                frame_count = 0

            delta_time = current_frame - last_frame
            last_frame = current_frame

            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            #color = tuple(self.config_dict['background_color'])
            glClearColor(*self.color)

            self.start_imgui_frame()
            self.menu()

            self.model = np.identity(4, dtype=np.float32)

            self.model[0][3] = 0.0
            self.model[1][3] = 0.0
            self.model[2][3] = self.camera.mouse_scroll

            self.model = np.dot(self.model, self.camera.rotation_matrix)
            self.draw_object()

            self.render_imgui()
            glfw.swap_buffers(self.window)

        self.shutdown_imgui()
        glfw.terminate()


def main():
    scene = App()
    scene.run()


if __name__ == "__main__":
    main()
