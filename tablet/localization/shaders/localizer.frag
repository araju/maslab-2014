varying float x;
varying float y;
uniform float width;
uniform float height;
uniform float distances[4];
uniform int firstTime; // to denote the first time this is run. TODO: make this obsolete
uniform sampler2D txtr;



// gives back a heat map that shows the best orientation and confidence for
// each position on the map

// in Blue channel - best orientation, measured 0 - 1. angle goes clockwise!!!
// in Red channel - confidence, as measured from 0 - 1.

// as input, the first row has 4 sensor measurements.
// the first 4 are the distances, the second 4 are the orientations. 

// the input texture is the distance transform

// TODO: take into account prior confidence, which will be stored in one of the channels


float dx = 1.0 / width; //convert from pixels to img coords
float dy = 1.0 / height;

vec2[4] initVectors() {

	float mToPixels = 100; //converts meters to pixels (100 pixels / m)
	vec2 dist[4];
		
	dist[0] = vec2(distances[0]*mToPixels,0.0);
	dist[1] = vec2(0.0,-distances[1]*mToPixels);
	dist[2] = vec2(-distances[2]*mToPixels,0.0);
	dist[3] = vec2(0.0,distances[3]*mToPixels);
	
	return dist;
}

// Need the conversion factor from physical distance to image coords
// It is 1 pixel = 1 cm
float getConfidence(vec2 dist[4]) {
	float total = 0.0;
	
	for (int i = 0; i < dist.length(); i++) {
		float a = x + dist[i].x*dx;
		float b = y + dist[i].y*dy;
		if (a < 0.0 || b < 0.0 || a > 1.0 || b > 1.0) {
			return 0.0;
		}
		total += texture(txtr, vec2(a,b),0.0).x;
	}	
	
	return (total / 4.0);
}


void main() {
	//don't do this for points that are on the walls
	float dt = texture(txtr,vec2(x,y),0.0).x;
	if (dt >= 1.0) {
		gl_FragColor = vec4(0.0,0.0,0.0,1);
		return;
	}
	
	//init some variables
	float dTheta = 0.09817477; // 2pi / 64. the rotation theta for the vectors
	mat2 rotMat = mat2(cos(dTheta), sin(dTheta), -sin(dTheta), cos(dTheta));
	
	vec2 vectors[4] = initVectors();
	float bestConfidence = 0.0;
	float bestOrientation = 0.0; // in radians
	for (int i = 11; i < 12; i++) {
		// calculate the confidence for this orientation
		float conf = getConfidence(vectors);
		if (conf > bestConfidence) {
			bestConfidence = conf;
			bestOrientation = dTheta*i;
		}
		//rotate the vectors
		for (int i = 0; i < vectors.length(); i++) {
			vectors[i] = rotMat * vectors[i];
		}
	}
	
	//take into account prior confidence
	if (firstTime != 1) {
		bestConfidence = bestConfidence * texture(txtr,vec2(x,y),0.0).y; //the prev conf
	}
	
	gl_FragColor = vec4(dt,bestConfidence,bestOrientation / 6.2832,1); // divide by 2*pi to normalize orientation 
	//gl_FragColor = vec4(vectors[3].x,vectors[3].x,vectors[3].x,1);
}