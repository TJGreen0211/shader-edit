import math
import numpy as np

def mat4_perspective(fovy, aspect, z_near, zFar):
	c = np.zeros((4, 4), dtype=np.float32)
	top = math.tan(fovy*(3.14159265358979323846 / 180.0)/2.0) * z_near
	right = top * aspect
	c[0][0] = z_near/right
	c[1][1] = z_near/top
	c[2][2] = -(zFar + z_near)/(zFar - z_near)
	c[2][3] = -2.0*zFar*z_near/(zFar - z_near)
	c[3][2] = -1.0
	c[3][3] = 0.0

	return c


print(mat4_perspective(90.0, 1280.0/720.0, 0.1, 5000.0))