from PIL import Image
import OpenGL.GL as opengl
import numpy as np

class Textures():
	def __init__(self, path):
		self.path = path
		self.image_width = 0
		self.image_height = 0
		self.icon_width = 0
		self.icon_height = 0
		self.texture_id = self.load_texture()
		self.icon_id = self.load_texture_icon()

	def _get_img_type(self, path):
		if self.path.split(".")[-1] == "png":
			img_type = opengl.GL_RGBA
		else:
			img_type = opengl.GL_RGB
		return img_type


	def load_texture(self):
		img = Image.open(self.path)
		if img.mode == 'RGBA':
			img_type = opengl.GL_RGBA
		else:
			img_type = opengl.GL_RGB

		self.image_width = img.size[0]
		self.image_height = img.size[1]
		#img = Image.open("resources/textures/earth_day.jpg")
		img_data = np.array(list(img.getdata()), np.uint8)
		texture = opengl.glGenTextures(1)
		opengl.glBindTexture(opengl.GL_TEXTURE_2D, texture)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_WRAP_S, opengl.GL_REPEAT)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_WRAP_T, opengl.GL_REPEAT)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MAG_FILTER, opengl.GL_LINEAR)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MIN_FILTER, opengl.GL_LINEAR)
		opengl.glTexImage2D(opengl.GL_TEXTURE_2D, 0, img_type, img.width, img.height, 0, img_type, opengl.GL_UNSIGNED_BYTE, img_data.tobytes())
		opengl.glEnable(opengl.GL_TEXTURE_2D)
		opengl.glBindTexture(opengl.GL_TEXTURE_2D, 0)

		return texture

	def load_texture_icon(self, icon_height=64):
		img = Image.open(self.path)
		if img.mode == 'RGBA':
			img_type = opengl.GL_RGBA
		else:
			img_type = opengl.GL_RGB
		
		wpercent = (icon_height/float(img.size[1]))
		hsize = int((float(img.size[0])*float(wpercent)))
		img = img.resize((hsize,icon_height), Image.ANTIALIAS)
		self.icon_width = img.size[0]
		self.icon_height = img.size[1]
		#img.save('somepic.jpg')
		#img = Image.open("resources/textures/earth_day.jpg")
		img_data = np.array(list(img.getdata()), np.uint8)
		texture = opengl.glGenTextures(1)
		opengl.glBindTexture(opengl.GL_TEXTURE_2D, texture)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_WRAP_S, opengl.GL_REPEAT)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_WRAP_T, opengl.GL_REPEAT)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MAG_FILTER, opengl.GL_LINEAR)
		opengl.glTexParameteri(opengl.GL_TEXTURE_2D, opengl.GL_TEXTURE_MIN_FILTER, opengl.GL_LINEAR)
		opengl.glTexImage2D(opengl.GL_TEXTURE_2D, 0, img_type, img.width, img.height, 0, img_type, opengl.GL_UNSIGNED_BYTE, img_data.tobytes())
		opengl.glEnable(opengl.GL_TEXTURE_2D)
		opengl.glBindTexture(opengl.GL_TEXTURE_2D, 0)

		return texture


#Textures().load_texture("/home/tj/Documents/code/shader-edit/resources/images/earth.jpeg")