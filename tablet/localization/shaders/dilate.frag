varying float x;
varying float y;
uniform float width;
uniform float height;
uniform sampler2D txtr;

// dilates the confidence channel (green channel)

void main() {
	float dx = 1.0/width;
	float dy = 1.0/height;
	
	int kernel_size = 15;
	float max = 0;
	
	for (int i = -kernel_size; i <= kernel_size; i++) {
		for (int j = -kernel_size; j <= kernel_size; j++) {
			float conf = texture(txtr,vec2(x+float(i)*dx,y+float(j)*dy),0.0).y;
			if (conf > max) {
				max = conf;
			}
		}
	}
	float dt = texture(txtr,vec2(x,y),0.0).x;
	float theta = texture(txtr,vec2(x,y),0.0).z;
	gl_FragColor = vec4(dt,max,theta,1);
}