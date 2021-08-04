

class Camera(object):
	def __init__(self, mouse_scroll = 0.0):
		self.mouse_scroll = mouse_scroll
		self.zoom_speed = 0.1
		self.mouse_sensitivity = 0.01
		self.last_x = 0
		self.last_y = 0
		
		self.yaw = 0.0
		self.pitch = 0.0


	def process_mouse_scroll(self, y_offset, delta_time):
		print(y_offset)
		
		if self.mouse_scroll < -20.0:
			self.mouse_scroll = -20.0
		if self.mouse_scroll >= -1.0:
			 self.mouse_scroll = -1.0
		
		
		self.mouse_scroll += y_offset*self.zoom_speed #delta_time*camera->zoom_speed;
		print(f"Mouse scroll: {self.mouse_scroll}")
		return y_offset

	def process_mouse_movement(self, x_pos, y_pos, reset_flag):
		if reset_flag:
			self.last_x = x_pos
			self.last_y = y_pos
		else:
			diff_x = x_pos - self.last_x
			diff_y = y_pos - self.last_y

			last_x = x_pos
			last_y = y_pos

			diff_x *= self.mouse_sensitivity
			diff_y *= self.mouse_sensitivity

			

			self.yaw += diff_x
			self.pitch += diff_y

			print(self.yaw, self.pitch)

