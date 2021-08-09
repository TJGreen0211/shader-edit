#version 330

layout (location = 0) in vec3 position;

out vec3 v_color;

uniform vec3 camera_position;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

void main() {
	gl_Position = vec4(position, 1.0)*view*model*projection;
	v_color = position.xyz;
}
 