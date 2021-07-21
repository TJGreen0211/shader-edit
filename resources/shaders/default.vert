uniform mat4 u_projection_mat;
attribute vec3 a_position;
varying vec4 v_color;
void main()
{
	gl_Position = u_projection_mat*vec4(a_position, 1.0);
	v_color = (vec4(a_position, 1.0)+1.0)/2.0;
}