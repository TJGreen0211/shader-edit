#version 450

in vec4 fPosition;
in mat4 m;
in vec2 tex_coord;

uniform vec3 camera_position;
uniform sampler2D texture0;
uniform float theta_time;

out vec4 FragColor;


vec3 rayDirection(vec3 cam, mat4 model) {
	vec4 ray = model*fPosition - vec4(cam, 1.0);
	return normalize(vec3(ray));
}


void main (void)
{
	vec3 dir = rayDirection(camera_position, m);
	vec3 eye = camera_position;
    

    vec2 sp =  tex_coord;
    float r = dot(sp,sp);
    float f = (1.0-sqrt(abs(1.0-r)))/(r) * 0.5;

    vec2 newUv;
    newUv.x = sp.x*f;
  	newUv.y = sp.y*f;
    newUv += vec2( theta_time/50.0, 0.0 );

    vec3 color = vec3(texture(texture0, tex_coord)).rgb;

	//vec3 l = normalize(lightPosition);
	//vec2 e = rayIntersection(eye, dir, fOuterRadius);
	//if ( e.x > e.y ) {
	//	discard;
	//}
	//vec2 f = rayIntersection(eye, dir, fInnerRadius);
	//e.y = min(e.y, f.x);
	//
	//vec3 I = inScatter(eye, dir, e, l);
	
	FragColor = vec4(color, 1.0);
}