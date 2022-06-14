//https://www.shadertoy.com/view/MsVXWW

#version 450

uniform float E; // Sun brightness
uniform float K_R; // Rayleigh constant > thicker
uniform float K_M; // Mie constant > thicker
uniform float G_M; // Gravity
uniform vec3 C_R;
uniform vec3 camera_position;
uniform vec3 lightPosition;
uniform float theta_time;

in vec4 fPosition;
//in vec3 fNormal;
in mat4 m;
in mat4 v;

out vec4 FragColor;

const float PI = 3.14159265359;
const float degToRad = PI / 180.0;
const float MAX = 10000.0;

const float DEG_TO_RAD = PI / 180.0;
//float K_R = 0.166;
//const float K_M = 0.0025;
//const float E = 14.3;//Sun brightness
//const vec3 C_R = vec3(0.3, 0.7, 1.0);
//const float G_M = -0.85;

uniform float fInnerRadius;
uniform float fOuterRadius;

float SCALE_H = 4.0 / (fOuterRadius - fInnerRadius);
float SCALE_L = 1.0 / (fOuterRadius - fInnerRadius);

const int numOutScatter = 5;
const float fNumOutScatter = 5.0;
const int numInScatter = 5;
const float fNumInScatter = 5.0;


#define pi 3.14159265
#define R(p, a) p=cos(a)*p+sin(a)*vec2(p.y, -p.x)

float rand(vec2 co)
{
	return fract(sin(dot(co*0.123,vec2(12.9898,78.233))) * 43758.5453);
}

vec3 rayDirection(vec3 cam) {
	vec4 ray = m*fPosition - vec4(cam, 1.0);
	return normalize(vec3(ray));
}

vec2 rayIntersection(vec3 p, vec3 dir, float radius ) {
	float b = dot( p, dir );
	float c = dot( p, p ) - radius * radius;
	
	float d = b * b - c;
	if ( d < 0.0 ) {
		return vec2( MAX, -MAX );
	}
	d = sqrt( d );
	
	float near = -b - d;
	float far = -b + d;
	
	return vec2(near, far);
}

//vec3 inScatter(vec3 o, vec3 dir, vec2 e, vec3 l) {
//	float len = (e.y - e.x) / fNumInScatter;
//	vec3 step = dir * len;
//	vec3 p = o + dir * e.x;
//	vec3 v = p + dir * (len * 0.5);
//	
//	vec3 sum = vec3(0.0);
//	for(int i = 0; i < numInScatter; i++) {	
//		vec2 f = rayIntersection(v, l, fOuterRadius);
//		vec3 u = v + l * f.y;
//		float n = (optic(p, v) + optic(v, u))*(PI * 4.0);
//		sum += density(v)* exp(-n * ( K_R * C_R + K_M ));
//		v += step;
//	}
//	sum *= len * SCALE_L;
//	float c = dot(dir, -l);
//	float cc = c * c;
//	return sum * ( K_R * C_R * rayleighPhase( cc ) + K_M * miePhase( G_M, c, cc ) ) * E;
//}

const float nudge = 0.739513;	// size of perpendicular vector
float normalizer = 1.0 / sqrt(1.0 + nudge*nudge);	// pythagorean theorem on that perpendicular to maintain scale
float SpiralNoiseC(vec3 p)
{
    float n = 0.0;	// noise amount
    float iter = 1.0;
    for (int i = 0; i < 8; i++)
    {
        // add sin and cos scaled inverse with the frequency
        n += -abs(sin(p.y*iter) + cos(p.x*iter)) / iter;	// abs for a ridged look
        // rotate by adding perpendicular and scaling down
        p.xy += vec2(p.y, -p.x) * nudge;
        p.xy *= normalizer;
        // rotate on other axis
        p.xz += vec2(p.z, -p.x) * nudge;
        p.xz *= normalizer;
        // increase the frequency
        iter *= 1.733733;
    }
    return n;
}

float SpiralNoise3D(vec3 p)
{
    float n = 0.0;
    float iter = 1.0;
    for (int i = 0; i < 5; i++)
    {
        n += (sin(p.y*iter) + cos(p.x*iter)) / iter;
        p.xz += vec2(p.z, -p.x) * nudge;
        p.xz *= normalizer;
        iter *= 1.33733;
    }
    return n;
}

float NebulaNoise(vec3 p)
{
	//p = p+(theta_time/500.0);
	float final = p.y + 4.5;
	p = p.xyz*1.5;
    final -= SpiralNoiseC(p.xyz);   // mid-range noise
    final += SpiralNoiseC(p.zxy*0.5123)*4.0;   // large scale features
    final -= SpiralNoise3D(p);   // more large scale features, but 3d

	//final = pow(final, 1.0);

    return final;
}


float map(vec3 p) 
{
	//#ifdef ROTATION
	//R(p.xz, iMouse.x*0.008*pi+iTime*0.1);
	//#endif
    
	float NebNoise = abs(NebulaNoise(p/0.5)*0.5);
    
	return NebNoise+0.03;
}

vec3 computeColor( float density, float radius )
{
	// color based on density alone, gives impression of occlusion within
	// the media
	vec3 result = mix( vec3(1.0,0.9,0.8), vec3(0.4,0.15,0.1), density );
	
	// color added to the media
	vec3 colCenter = 7.*vec3(0.8,1.0,1.0);
	vec3 colEdge = 1.5*vec3(0.48,0.53,0.5);
	result *= mix( colCenter, colEdge, min( (radius+.05)/.9, 1.15 ) );
	
	return result;
}

vec3 ToneMapFilmicALU(vec3 _color)
{
	_color = max(vec3(0), _color - vec3(0.004));
	_color = (_color * (6.2*_color + vec3(0.5))) / (_color * (6.2 * _color + vec3(1.7)) + vec3(0.06));
	return _color;
}


void main (void)
{
	vec3 dir = rayDirection(camera_position);
	vec3 eye = camera_position;

	//R(dir.yz, -pi*3.93);
    //R(dir.xz, pi*3.2);
    //R(eye.yz, -pi*3.93);
   	//R(eye.xz, pi*3.2);    
	vec2 seed = fPosition.xy + fract(0.0);

	vec3 l = normalize(lightPosition);
	// ld, td: local, total density 
	// w: weighting factor
	float ld=0., td=0., w=0.;
	// t: length of the ray
	// d: distance function
	float d=1., t=0.;
	const float h = 0.8;
	vec4 sum = vec4(0.0);
	float min_dist=0.0, max_dist=0.0;

	vec2 e = rayIntersection(eye, dir, fOuterRadius);
	if(e.y > 0.0) {
		float len = (e.y - e.x) / 56.0;
		vec3 step_len = dir * len;
		vec3 p = eye + dir * e.x;
		vec3 v = p + dir * (len * 0.5);
		
		t = min_dist*step(t,min_dist);
		
		for (int i=0; i<56; i++) {
			
			if(td>0.9 || d<0.1*t || t>10. || sum.a > 0.99 || t>max_dist) break;
			
			//if(td>0.9 || d<0.1*t || t>10. || sum.a > 0.99 || t>max_dist) break;
			//float d = map(v+(theta_time/100.0));
			float d = map(v);
			

			d = max(d,0.08);
			vec3 ldst = vec3(0.0)-v;
			float lDist = max(length(ldst), 0.001);
			vec3 lightColor=vec3(1.0,0.5,0.25);
			sum.rgb+=(lightColor/(lDist*lDist)/300.);
			
			if (d<h) {
				ld = h - d;
				w = (1. - td) * ld;
				td += w + 1./200.;
				vec4 col = vec4( computeColor(td,lDist), td );
				col.a *= 0.185;
				col.rgb *= col.a;
				sum = sum + col*(1.0 - sum.a);  
			}
			td += 1./70.;
			d = max(d, 0.04); 
			d=abs(d)*(.8+0.2*rand(seed*vec2(i)));
			//t += max(d * 0.1 * max(min(length(ldst),length(eye)),1.0), 0.02);
			//v += max(d * 0.1 * max(min(length(ldst),length(eye)),1.0), 0.02);
			v += step_len*d;
			
		}
		sum *= 1. / exp( ld * 0.2 ) * 0.6;
		sum = clamp( sum, 0.0, 1.0 );
		sum.xyz = sum.xyz*sum.xyz*(3.0-2.0*sum.xyz);
		FragColor = vec4(sum.xyz, 1.0); 
		//FragColor =  vec4(ToneMapFilmicALU(sum.xyz*2.2),1.0);
		
		
	} else {
		FragColor = vec4(0.0, 0.0, 0.0, 1.0);
	}

	
	//FragColor = vec4(sn ,sn, sn, 1.0);
	//if ( e.x > e.y ) {
	//	discard;
	//}
	//vec2 f = rayIntersection(eye, dir, fInnerRadius);
	//e.y = min(e.y, f.x);
	
	//vec3 I = inScatter(eye, dir, e, l);
	
	//FragColor = vec4(I, 1.0);
}