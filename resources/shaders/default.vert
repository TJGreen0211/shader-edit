#version 330

in vec4 position;

out vec3 v_color;

uniform mat4 model;
uniform mat4 projection;

void main() {
	gl_Position = position*model*projection;
	v_color = position.xyz;
}
 