import math
import numpy as np

class Camera(object):
	def __init__(self, mouse_scroll = 0.0):
		self.mouse_scroll = mouse_scroll
		self.zoom_speed = 0.1
		self.mouse_sensitivity = 0.0001
		self.last_x = 0
		self.last_y = 0

		self.x = 0.0
		self.y = 0.0
		
		self.yaw = 0.0
		self.pitch = 0.0

		self.front = [0.0, 1.0, 0.0]
		self.right = [1.0, 0.0, 0.0]
		self.up = [0.0, 0.0, 1.0]

		self.rotation_matrix = np.identity(4, dtype=np.float32)

	def get_camera_position(self, position):
		p = np.identity(4, dtype=np.float32)
		# Need only the position part of the matrix
		p[0][3] = position[0][3]
		p[1][3] = position[1][3]
		p[2][3] = position[2][3]
		mv_transpose = np.dot(p, np.identity(4, dtype=np.float32)).transpose()
		inverse_camera = [-mv_transpose[3][0], -mv_transpose[3][1], -mv_transpose[3][2], -mv_transpose[3][3]]
		cam_position = np.dot(mv_transpose, inverse_camera)

		return cam_position


	def process_mouse_scroll(self, y_offset, delta_time):
		
		if self.mouse_scroll < -20.0:
			self.mouse_scroll = -20.0
		if self.mouse_scroll >= -1.0:
			 self.mouse_scroll = -1.0
		
		
		self.mouse_scroll += y_offset*self.zoom_speed #delta_time*camera->zoom_speed
		return y_offset

	def reset_view(self):
		self.rotation_matrix = np.identity(4, dtype=np.float32)
	
	def update_camera_vectors(self):
		rad = 180.0 / math.pi

		self.front[0] = math.cos(self.yaw) * math.cos(self.pitch)
		self.front[1] = math.sin(self.pitch)
		self.front[2] = math.sin(self.yaw ) * math.cos(self.pitch)
		self.front = self.front / np.sqrt(np.sum([x**2.0 for x in self.front]))#vec3Normalize(self.front)

		arc_yaw = -math.asin(-self.front[1]) * rad
		arc_pitch = -math.atan2(self.front[0], -self.front[2]) * rad

		rot_x = np.identity(4, dtype=np.float32)
		rot_x[2][2] = rot_x[1][1] = math.cos(arc_yaw)
		rot_x[2][1] = math.sin(arc_yaw)
		rot_x[1][2] = -rot_x[2][1]

		rot_y = np.identity(4, dtype=np.float32)
		rot_y[2][2] = rot_y[0][0] = math.cos(arc_pitch)
		rot_y[0][2] = math.sin(arc_pitch)
		rot_y[2][0] = -rot_y[0][2]

		self.rotation_matrix = np.dot(rot_x, rot_y)
		#self.rotation_matrix = mat4Multiply(mat4RotateX(arc_yaw), mat4RotateY(arc_pitch))
		#
		self.right[0] = self.rotation_matrix[0][0]    
		self.right[1] = self.rotation_matrix[0][1]
		self.right[2] = self.rotation_matrix[0][2]
		self.right / np.sqrt(np.sum([x**2.0 for x in self.right]))
		#self.right = vec3Normalize(self.right)
		#
		self.up[0] = self.rotation_matrix[1][0]    
		self.up[1] = self.rotation_matrix[1][1]
		self.up[2] = self.rotation_matrix[1][2]
		self.right / np.sqrt(np.sum([x**2.0 for x in self.up]))
		#self.up = vec3Normalize(self.up)

		#camera->right = vec3Normalize(crossProduct(camera->front, camera->up))
		#camera->up = vec3Normalize(crossProduct(camera->right, camera->front))


	def process_mouse_movement(self, x_pos, y_pos, reset_flag):
		if reset_flag:
			self.last_x = x_pos
			self.last_y = y_pos
		else:
			diff_x = x_pos - self.last_x
			diff_y = y_pos - self.last_y

			self.last_x = x_pos
			self.last_y = y_pos

			diff_x *= self.mouse_sensitivity
			diff_y *= self.mouse_sensitivity

			self.yaw += diff_x
			self.pitch += diff_y

			self.update_camera_vectors()

