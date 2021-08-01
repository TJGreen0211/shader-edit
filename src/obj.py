import os


def object_load(obj_path):
	vertices = []
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

	verts = []

	for i in range(int(len(faces) / (3))):
		fi = i * 3
		a = (faces[fi+0]-1)*3
		b = (faces[fi+1]-1)*3
		c = (faces[fi+2]-1)*3

		verts.append(vertices[a+0]); 
		verts.append(vertices[a+1]); 
		verts.append(vertices[a+2]); 

		verts.append(vertices[b+0]); 
		verts.append(vertices[b+1]); 
		verts.append(vertices[b+2]); 

		verts.append(vertices[c+0]); 
		verts.append(vertices[c+1]); 
		verts.append(vertices[c+2]); 

	return verts
