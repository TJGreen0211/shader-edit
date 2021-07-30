#version 330

in vec4 position;

uniform mat4 model;
uniform mat4 projection;

void main() {
	gl_Position = position*model*projection;
}
 