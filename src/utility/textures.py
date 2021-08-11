from PIL import Image
import OpenGL.GL as opengl
import numpy as np

class Textures():
	def load_texture(self, path):
		img = Image.open(path)
		#img = Image.open("resources/textures/earth_day.jpg")
		img_data = np.array(list(img.getdata()), np.uint8)
		texture = opengl.glGenTextures(1)
		opengl.glBindTexture(opengl.GL_TEXTURE_2D, texture)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_WRAP_S, opengl.GL_REPEAT)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_WRAP_T, opengl.GL_REPEAT)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MAG_FILTER, opengl.GL_LINEAR)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MIN_FILTER, opengl.GL_LINEAR)
		opengl.glTexImage2D(opengl.GL_TEXTURE_2D, 0, opengl.GL_RGB, img.width, img.height, 0, opengl.GL_RGB, opengl.GL_UNSIGNED_BYTE, img_data.tobytes())
		opengl.glEnable(opengl.GL_TEXTURE_2D)
		opengl.glBindTexture(opengl.GL_TEXTURE_2D, 0)

		return texture


print(Textures().load_texture("/home/tj/Documents/code/shader-edit/resources/images/noise1.png"))