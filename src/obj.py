import os

class ObjectLoader(object):
	def __init__(self):
		self.vertices = []
		self.normals = []
		self.texture_coords = []
		self.faces = []


	def load_object(self, obj_path):
		vertices = []
		normals = []
		texture_coords = []
		faces = []
		for line in open(obj_path, "r"):
			if line.startswith('#'):
				continue
			if line.startswith('s'):
				continue
			values = line.split()
			if not values:
				continue
			if values[0] == 'v':
				for v in values[1:]:
					vertices.append(float(v))
			elif values[0] == 'f':
				for v in values[1:]:
					w = v.split('/')
					faces.append(int(w[0]))
					if len(w) == 3:
						texture_coords.append(int(w[1]))
						normals.append(int(w[2]))
	

		for i in range(int(len(faces) / (3))):
			fi = i * 3
			a = (faces[fi+0]-1)*3
			b = (faces[fi+1]-1)*3
			c = (faces[fi+2]-1)*3

			self.vertices.append(vertices[a+0]); self.normals.append(normals[a+0]); self.texture_coords.append(texture_coords[a+0])
			self.vertices.append(vertices[a+1]); self.normals.append(normals[a+1]); self.texture_coords.append(texture_coords[a+1])
			self.vertices.append(vertices[a+2]); self.normals.append(normals[a+2]); 

			self.vertices.append(vertices[b+0]); self.normals.append(normals[b+0]); self.texture_coords.append(texture_coords[b+0])
			self.vertices.append(vertices[b+1]); self.normals.append(normals[b+1]); self.texture_coords.append(texture_coords[b+1])
			self.vertices.append(vertices[b+2]); self.normals.append(normals[b+2]); 

			self.vertices.append(vertices[c+0]); self.normals.append(normals[c+0]); self.texture_coords.append(texture_coords[b+0])
			self.vertices.append(vertices[c+1]); self.normals.append(normals[c+1]); self.texture_coords.append(texture_coords[b+1])
			self.vertices.append(vertices[c+2]); self.normals.append(normals[c+2]); 

		return self.vertices
