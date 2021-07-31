
import glfw

from OpenGL.GL import *
from gui import GUI

#from scene import Scene


class App(GUI):
	def __init__(self):
		super().__init__()

	def run(self):
		frame_count = 0
		time_count = 0.0
		last_frame = 0.0

		#color = (0.1, 0.5, 0.7, 1.0)
		
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
			glClear(GL_COLOR_BUFFER_BIT)

			#color = tuple(self.config_dict['background_color'])
			glClearColor(*self.color)


			self.start_imgui_frame()
			self.menu()

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
	