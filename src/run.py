"""Runs the main application."""
import glfw

from OpenGL.GL import *
from gui.gui import GUI


class App(GUI):
    """Main Application."""

    def _gl_enable(self):
        glDisable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)

    def _calculate_fps(self):
        # TODO: Move this out of the main function
        pass

    def run(self):
        """Run the application."""
        frame_count = 0
        time_count = 0.0
        last_frame = 0.0
        theta = 0.0

        self._gl_enable()

        while not glfw.window_should_close(self.window):
            if self.enable_blend:
                glEnable(GL_BLEND)
                glBlendFunc(GL_ONE, GL_ONE)
            else:
                glDisable(GL_BLEND)

            if self.enable_cull_face:
                glEnable(GL_CULL_FACE)
            else:
                glDisable(GL_CULL_FACE)

            frame_count += 1
            current_frame = glfw.get_time()
            if(current_frame - time_count >= 1.0):
                self.fps_values.pop(0)
                self.fps_values.append(frame_count)
                time_count = current_frame
                frame_count = 0

            delta_time = current_frame - last_frame
            theta = theta + 1.0 * delta_time
            last_frame = current_frame

            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glClearColor(*self.color)

            self.start_imgui_frame()
            self.menu()

            self.draw_object(self.uniform_dict, self.textures_list, theta)

            self.render_imgui()
            glfw.swap_buffers(self.window)

        self.shutdown_imgui()
        glfw.terminate()


def main():
    """Main"""
    scene = App()
    scene.run()


if __name__ == "__main__":
    main()
