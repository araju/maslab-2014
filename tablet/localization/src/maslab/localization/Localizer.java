package maslab.localization;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.imageio.ImageIO;

import Core.Engine;
import Core.FilterOp;

public class Localizer {

	public static final int confidenceThresh = 245; // only points above this in the green channel
													// are considered confident
	
	private BufferedImage currentImage; // keeps track of the most recent filtered image
										// lets us have frame to frame memory
	
	
	
	private boolean firstTime = true;  // "like a virgin..."
	private int maxConf = 0;
	
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
	
	public BufferedImage getImage() {
		return this.currentImage;
	}
	
	
	public List<List<Float>> processSensorMeasurements(float[] sensorMeasurements) {
		
		FilterOp localizer = new FilterOp("localizer");
		localizer.setFloatArray("distances", sensorMeasurements);
		
		if (!firstTime) {
			localizer.setInt("firstTime", 0);
			// rescale confidence channel
			FilterOp rescaler = new FilterOp("rescaleConfidence");
			FilterOp dilater = new FilterOp("dilate");
			if (maxConf != 0) {
				rescaler.setFloat("rescaleFactor", (float) (255.0 / maxConf));
			} else {
				rescaler.setFloat("rescaleFactor", (float)1.0);
			}
			rescaler.apply(currentImage);
			// dilate confidence channel
			dilater.apply();
			localizer.apply();
		} else {
			localizer.setInt("firstTime", 1);
			localizer.apply(this.currentImage);
			firstTime = false;
		}
		
		this.currentImage = FilterOp.getImage(); // R - orientation , G - confidence , B - distance to edge(wall)
		
		return getConfidentPoints();
	}
	
	
	/**
	 * Does the thresholding to return the points that we might be at. 
	 * For now returns points in IMG COORDINATES!!!!
	 * For x,y, thats 0,0 at top left and heading of 0 points down x-axis  
	 * 
	 * Also finds max confidence value and re-scales all confident points 
	 * to full confidence 
	 * 
	 * @param img - filtered image
	 * @return list of [x,y,heading] in image coordinates
	 */
	public List<List<Float>> getConfidentPoints() {
		List<List<Float>> confidentPts = new ArrayList<List<Float>>();
		int w = currentImage.getWidth();
	    int h = currentImage.getHeight();

	    int[] data = currentImage.getRGB(0, 0, w, h, null, 0, w);
	    
	    maxConf = 0;
	    
	    for (int i = 0; i < data.length; i++) {
	    	int red = (data[i] >> 16) & 0xFF;
	    	int green = (data[i] >> 8) & 0xFF;
	    	int blue = (data[i]) & 0xFF;
	    	int alpha = (data[i] >> 24) & 0xFF;
	    	
	    	if (green > maxConf) {
	    		maxConf = green;
	    	}
	    	
	    	if (green >= confidenceThresh) {
	    		int x = i % w;
	    		int y = i / w;
	    		ArrayList<Float> arr = new ArrayList<Float>();
	    		arr.add((float)x);
	    		arr.add((float)y);
	    		arr.add((float) (red  / 255.0 * 360)); // theta
	    		confidentPts.add(arr);
	    		
	    		// set to max confidence to get ready for next iteration.
	    		currentImage.setRGB(x, y, new Color(red,255,blue,alpha).getRGB());
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
			image = ImageIO.read(new File("C:\\Users\\akhil\\Documents\\MASLAB\\shadercl\\ShaderCL\\ShaderCL Examples\\images\\map_dt2.png"));
		} catch (IOException e) {
			e.printStackTrace();
		}
		Localizer local = new Localizer(image);
		float start = System.currentTimeMillis();
		local.processSensorMeasurements(new float[] {
				(float)0.7196930784229848,
				(float)0.5821820280118326,
				(float)0.5769988321789806,
				(float)0.7957202438799321
		});
		List<List<Float>> pts = local.getConfidentPoints();
		float end = System.currentTimeMillis();
		
		System.out.println((end - start) + "\n\n");
		
		System.out.println("Number of pts: " + pts.size());
		
		try {
		    File outputfile = new File("filtered_dt.png");
		    ImageIO.write(local.getImage(), "png", outputfile);
		} catch (IOException e) {
			e.printStackTrace();
		}
//		for (float[] arr : pts) {
//			System.out.println(arr[0] + " " + arr[1] + " " + arr[2]);
//		}

	}

}
