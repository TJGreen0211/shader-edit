//https://www.shadertoy.com/view/XlcSDr

#version 450

uniform vec3 camera_position;
uniform vec3 lightPosition;
uniform float theta_time;

in vec4 fPosition;
in mat4 m;
in mat4 v;

out vec4 FragColor;

uniform float fInnerRadius;
uniform float fOuterRadius;

const int   STAR_FIELD_VOXEL_STEPS = 22;
const float PI = 3.14159265359;
const float MAX = 10000.0;

uniform sampler2D texture0;

vec3 rayDirection(vec3 cam, mat4 model) {
	vec4 ray = model*fPosition - vec4(cam, 1.0);
	return normalize(vec3(ray));
}

vec2 raySphereIntersect(vec3 p, vec3 dir, float radius ) {
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

/*
vec3 inScatter(vec3 o, vec3 dir, vec2 e, vec3 l) {
	float len = (e.y - e.x) / fNumInScatter;
	vec3 step = dir * len;
	vec3 p = o + dir * e.x;
	vec3 v = p + dir * (len * 0.5);
	
	vec3 sum = vec3(0.0);
	for(int i = 0; i < numInScatter; i++) {	
		vec2 f = rayIntersection(v, l, fOuterRadius);
		vec3 u = v + l * f.y;
		float n = (optic(p, v) + optic(v, u))*(PI * 4.0);
		sum += density(v)* exp(-n * ( K_R * C_R + K_M ));
		v += step;
	}
	sum *= len * SCALE_L;
	float c = dot(dir, -l);
	float cc = c * c;
	return sum * ( K_R * C_R * rayleighPhase( cc ) + K_M * miePhase( G_M, c, cc ) ) * E;
}*/

#define HASHSCALE1 .1031
float hash(float p)
{
	vec3 p3  = fract(vec3(p) * HASHSCALE1);
    p3 += dot(p3, p3.yzx + 19.19);
    return fract((p3.x + p3.y) * p3.z);
}
float hash(vec3 p3)
{
	p3  = fract(p3 * HASHSCALE1);
    p3 += dot(p3, p3.yzx + 19.19);
    return fract((p3.x + p3.y) * p3.z);
}

float pn(const in vec3 x) {
    vec3 p = floor(x), f = fract(x);
	f *= f*(3.-f-f);
	vec2 uv = (p.xy+vec2(37.,17.)*p.z) + f.xy,
	     rg = textureLod( texture0, (uv+.5)/256., -100.).yx;
	return 2.4*mix(rg.x, rg.y, f.z)-1.;
}

#define SPIRAL_NOISE_ITER 6
const float nudge = 20.;	// size of perpendicular vector
float normalizer = 1.0 / sqrt(1.0 + nudge*nudge);	// pythagorean theorem on that perpendicular to maintain scale
float SpiralNoiseC(vec3 p, vec4 id) {
    float iter = 2., n = 2.-id.x; // noise amount
    for (int i = 0; i < SPIRAL_NOISE_ITER; i++) {
        n += -abs(sin(p.y*iter) + cos(p.x*iter)) / iter; // add sin and cos scaled inverse with the frequency (abs for a ridged look)
        p.xy += vec2(p.y, -p.x) * nudge; // rotate by adding perpendicular and scaling down
        p.xy *= normalizer;
        p.xz += vec2(p.z, -p.x) * nudge; // rotate on other axis
        p.xz *= normalizer;  
        iter *= id.y + .733733;          // increase the frequency
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

float mapIntergalacticCloud(vec3 p, vec4 id) {
	//p = p+(theta_time/1.0);
	float k = 2.*id.w +.1;  // p/=k;
    return k*(.5 + SpiralNoiseC(p.zxy*.4132+333., id)*3. + pn(p*8.5)*.12);
	//float final = p.y + 4.5;
	//p = p.xyz*1.5;
    //final -= SpiralNoiseC(p.xyz, id);   // mid-range noise
    //final += SpiralNoiseC(p.zxy*0.5123+(theta_time/50.0), id)*4.0;   // large scale features
    //final -= SpiralNoise3D(p);   // more large scale features, but 3d

    //return final;
}

vec3 hsv2rgb(float x, float y, float z) {	
	return z+z*y*(clamp(abs(mod(x*6.+vec3(0,4,2),6.)-3.)-1.,0.,1.)-1.);
}

vec4 renderIntergalacticClouds(vec3 ro, vec3 rd, float tmax, const vec4 id) {
    
    float max_dist= min(tmax, float(STAR_FIELD_VOXEL_STEPS)),
		  td=0., d, t, noi, lDist, a, sp = 9.,         
    	  rRef = 2.*id.x,
          h = .05+.25*id.z;
    vec3 pos, lightColor;   
    vec4 sum = vec4(0);
   	
    t = .1*hash(hash(rd)); 

	//float len = (e.y - e.x) / fNumInScatter;
	//vec3 step = dir * len;
	//vec3 p = o + dir * e.x;
	//vec3 v = p + dir * (len * 0.5);

    for (int i=0; i<100; i++)  {
	    if(td>.9 ||  sum.a > .99 || t>max_dist) break;
        a = smoothstep(max_dist,0.,t);
        pos = ro + t*rd;
        d = abs(mapIntergalacticCloud(pos, id))+.07;

        // Light calculations
        lDist = max(length(mod(pos+sp*.5,sp)-sp*.5), .001); // TODO add random offset
        noi = pn(.05*pos);
        lightColor = mix(hsv2rgb(noi,.5,.6), 
                         hsv2rgb(noi+.3,.5,.6), 
                         smoothstep(rRef*.5,rRef*2.,lDist));
        sum.rgb += a*lightColor/exp(lDist*lDist*lDist*.08)/30.;
//		// Edges coloring
        if (d<h) {
			td += (1.-td)*(h-d)+.005;  // accumulate density
            sum.rgb += sum.a * sum.rgb * .25 / lDist;  // emission	
			sum += (1.-sum.a)*.02*td*a;  // uniform scale density + alpha blend in contribution 
        } 
        td += .015;
        t += max(d * .08 * max(min(lDist,d),2.), .01);  // trying to optimize step size
    }
//    
   	sum = clamp(sum, 0., 1.);   
    sum.xyz *= sum.xyz*(3.-sum.xyz-sum.xyz);
	return sum;
//	return vec4(lightColor, 1.0);
}


void main (void)
{
	vec3 dir = rayDirection(camera_position, m);
	vec3 eye = camera_position;

	//vec3 l = normalize(lightPosition);
	vec2 e = raySphereIntersect(eye, dir, fOuterRadius);

	float dStar = 9999.;
	vec4 clouds = renderIntergalacticClouds(eye, dir, dStar, vec4(0.5,0.4,0.16,0.7));
	
	FragColor = vec4(clouds.xyz, 1.0);
}