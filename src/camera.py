

class Camera(object):
	def __init__(self, mouse_scroll = 0.0):
		self.mouse_scroll = mouse_scroll
		self.zoom_speed = 0.1


	def process_mouse_scroll(self, y_offset, delta_time):
		print(y_offset)
		
		if self.mouse_scroll < -20.0:
			self.mouse_scroll = -20.0
		if self.mouse_scroll >= -1.0:
			 self.mouse_scroll = -1.0
		
		
		self.mouse_scroll += y_offset*self.zoom_speed #delta_time*camera->zoom_speed;
		print(f"Mouse scroll: {self.mouse_scroll}")
		return y_offset
