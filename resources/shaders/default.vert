#version 330

in vec4 position;

out vec3 v_color;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

void main() {
	gl_Position = position*view*model*projection;
	v_color = position.xyz;
}
 