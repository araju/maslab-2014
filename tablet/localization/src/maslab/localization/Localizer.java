package maslab.localization;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.imageio.ImageIO;

import Core.Engine;
import Core.FilterOp;

public class Localizer {

	public static final int confidenceThresh = 250; // only points above this in the green channel
													// are considered confident
	
	private BufferedImage currentImage; // keeps track of the most recent filtered image
										// lets us have frame to frame memory
	
	public Localizer() {
		this.currentImage = null;
	}
	
	public Localizer(BufferedImage initImg) {
		this.currentImage = initImg;
		if (initImg != null)
			Engine.initGL(initImg.getWidth(),initImg.getHeight());
	}
	
	public void setImage(BufferedImage img) {
		this.currentImage = img;
		if (img != null)
			Engine.initGL(img.getWidth(),img.getHeight());
	}
	
	
	public List<List<Float>> processSensorMeasurements(float[] sensorMeasurements) {
		FilterOp localizer = new FilterOp("localizer");
		
		localizer.setFloatArray("distances", sensorMeasurements);
		localizer.apply(this.currentImage);
		BufferedImage filtered = FilterOp.getImage(); // R - orientation , G - confidence , B - distance to edge(wall)
		
		// TODO: change the current image to reflect the changes in what we know
		//  maybe that includes blurring or dilating the confidence or something
		
		return getConfidentPoints(filtered);
	}
	
	
	/**
	 * Does the thresholding to return the points that we might be at. 
	 * For now returns points in IMG COORDINATES!!!!
	 * For x,y, thats 0,0 at top left and heading of 0 points down x-axis  
	 * 
	 * @param img - filtered image
	 * @return list of [x,y,heading] in image coordinates
	 */
	public List<List<Float>> getConfidentPoints(BufferedImage img) {
		List<List<Float>> confidentPts = new ArrayList<List<Float>>();
		int w = img.getWidth();
	    int h = img.getHeight();

	    int[] data = img.getRGB(0, 0, w, h, null, 0, w);
	    
	    for (int i = 0; i < data.length; i++) {
	    	int red = (data[i] >> 16) & 0xFF;
	    	int green = (data[i] >> 8) & 0xFF;
	    	
	    	if (green > confidenceThresh) {
	    		ArrayList<Float> arr = new ArrayList<Float>();
	    		arr.add((float) (i % w)); // x
	    		arr.add((float) (i / w)); // y
	    		arr.add((float) (red  / 255.0 * 360)); // theta
	    		confidentPts.add(arr);
	    	}
	    }
	    return confidentPts;
		
	}
	
	/**
	 * main method only for testing
	 */
	public static void main(String[] args) {
		//time it
		BufferedImage image = null;
		try {
			image = ImageIO.read(new File("C:\\Users\\akhil\\Documents\\MASLAB\\shadercl\\ShaderCL\\ShaderCL Examples\\images\\rainbow.png"));
		} catch (IOException e) {
			e.printStackTrace();
		}
		Localizer local = new Localizer(image);
		float start = System.currentTimeMillis();
		List<List<Float>> pts = local.getConfidentPoints(image);
		float end = System.currentTimeMillis();
		
		System.out.println((end - start) + "\n\n");
		
		System.out.println("Number of pts: " + pts.size());
//		for (float[] arr : pts) {
//			System.out.println(arr[0] + " " + arr[1] + " " + arr[2]);
//		}

	}

}
