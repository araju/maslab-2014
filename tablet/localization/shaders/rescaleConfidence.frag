varying float x;
varying float y;
uniform float width;
uniform float height;
uniform sampler2D txtr;
uniform float rescaleFactor;

//rescales all the confidence values by the previous max confidence
// this is to prevent all the confidences to slowly to go to zero
// after some time (since they are all <= 1.0 and get multiplied with
// each other from frame to frame)

void main() {
	float r = rescaleFactor;
	vec4 current = texture(txtr,vec2(x,y),0.0);
	float newConf = current.y * r;
	if (newConf >= 1.0) {
		newConf = 1.0;
	}
	gl_FragColor = vec4(current.x, newConf, current.z, 1);
}