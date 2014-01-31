package maslab.vision;

import java.io.File;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;

public class FrameProcessor {

//	private static final Scalar lowerBlue = new Scalar(90, 100, 50);
//	private static final Scalar upperBlue = new Scalar(115, 255, 255);
	
//	private static final Scalar lowerGreen = new Scalar(55, 80, 10);
//	private static final Scalar upperGreen = new Scalar(90, 255, 255);
	
//	private static final Scalar lowerRed = new Scalar(0, 100, 10);
//	private static final Scalar upperRed = new Scalar(15, 255, 255);
	
	private static final int ORIG_IMG_HEIGHT = 480;
	private static final int ORIG_IMG_WIDTH = 640;
	private static final int IMG_HEIGHT = 240;
	private static final int IMG_WIDTH = 320;
	private static final double RESIZE_FACTOR = 0.5;
	
	private static final Scalar lowerRed = new Scalar(110, 100, 10);
	private static final Scalar upperRed = new Scalar(130, 255, 255);
	
	private static final Scalar lowerGreen = new Scalar(35, 80, 10);
	private static final Scalar upperGreen = new Scalar(60, 255, 255);
	
	private static final Scalar lowerBlue = new Scalar(0, 100, 50);
	private static final Scalar upperBlue = new Scalar(20, 255, 255);
	
	private static final Scalar lowerTeal = new Scalar(20, 100, 50);
	private static final Scalar upperTeal = new Scalar(33, 255, 255);
	
	private static final Scalar lowerYellow = new Scalar(75,90,70);
	private static final Scalar upperYellow = new Scalar(95,255,255);
	
	private static final Scalar lowerPurple = new Scalar(131, 40, 40);
	private static final Scalar upperPurple = new Scalar(200, 255, 255);
	
	private static final int contourAreaThresh = 15;
	private static final int cleanKernelSize = 5;
	private static final int numBuffers = 15; //0: HSV, 1: Red Thresh, 2: Green, 3: Blue, 4: Teal
											 // 5,6,7,8: cleaned Red, Green, Blue, Teal, Yellow
											  // 9, Yellow Thresh, 10: Yellow cleaned
											  // 11: Purple thresh, 12: Purple cleaned
											  // 13: The bitwise or of the blue, teal, yellow, purple
											// 14: resized image
	
	private List<Mat> buffers = null;
	private Mat cleanKernel;
	
	static {
//		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
		loadLibrary();
	}
	
	public FrameProcessor() {
		buffers = new ArrayList<Mat>();
		for (int i = 0; i < numBuffers; i++) {
			buffers.add(new Mat());
		}
		
		cleanKernel = Mat.ones(cleanKernelSize, cleanKernelSize, CvType.CV_8U);
	}

	
	public Mat testThresh(Mat frame) {
		Mat ret = new Mat();
		Mat temp = new Mat();
		Imgproc.cvtColor(frame, temp, Imgproc.COLOR_BGR2HSV);
		Core.inRange(temp, lowerBlue, upperBlue, ret);
		return ret;
	}
	
	// returns map of color to list of blobs' centers, (x,y) in img coordinates. colors: red, green, blue
	public Map<String,List<double[]>> processFrame(Mat frame, Mat processedFrame) {
		Imgproc.resize(frame, buffers.get(14), new Size(IMG_WIDTH, IMG_HEIGHT));
		//first convert to hsv, store it in the first buffer
		Imgproc.cvtColor(buffers.get(14), buffers.get(0), Imgproc.COLOR_BGR2HSV);
		Core.inRange(buffers.get(0), lowerRed, upperRed, buffers.get(1));
		Core.inRange(buffers.get(0), lowerGreen, upperGreen, buffers.get(2));
		Core.inRange(buffers.get(0), lowerBlue, upperBlue, buffers.get(3));
		Core.inRange(buffers.get(0), lowerTeal, upperTeal, buffers.get(4));
		Core.inRange(buffers.get(0), lowerYellow, upperYellow, buffers.get(9));
		Core.inRange(buffers.get(0), lowerPurple, upperPurple, buffers.get(11));
		//clean thresholded images
		Imgproc.morphologyEx(buffers.get(1), buffers.get(5), Imgproc.MORPH_OPEN, cleanKernel); // Red
		Imgproc.morphologyEx(buffers.get(2), buffers.get(6), Imgproc.MORPH_OPEN, cleanKernel); // Green
		Imgproc.morphologyEx(buffers.get(3), buffers.get(7), Imgproc.MORPH_OPEN, cleanKernel); // Blue
		Imgproc.morphologyEx(buffers.get(4), buffers.get(8), Imgproc.MORPH_OPEN, cleanKernel); // Teal
		Imgproc.morphologyEx(buffers.get(9), buffers.get(10), Imgproc.MORPH_OPEN, cleanKernel); // Yellow
		Imgproc.morphologyEx(buffers.get(11), buffers.get(12), Imgproc.MORPH_OPEN, cleanKernel);  //Purple
//		buffers.set(8, processedFrame);
		
		Map<String,List<double[]>> blobs = new HashMap<String, List<double[]>>();
//		List<double[]> wall = findWalls(buffers.get(7).submat(0, 470, 240, 400)); // WARNING: USING FIXED NUMBERS!!!
//		double wallY = 0.0;
//		if (wall.size() > 0) {
//			blobs.put("blue", wall.subList(0, 1));
//			wallY = wall.get(1)[0];
//		} else {
//			blobs.put("blue", wall);
//		}
		
		// or the yellow, teal, and blue masks:
		Core.bitwise_or(buffers.get(7), buffers.get(8), buffers.get(13)); // blue or teal
		Core.bitwise_or(buffers.get(13), buffers.get(10), buffers.get(13)); //(blue or teal) or yellow
		Core.bitwise_or(buffers.get(13), buffers.get(12), buffers.get(13)); //(blue or teal or yellow) or purple
		
		
//		buffers.set(11, processedFrame);
		
		double[] wallYVals = findWallY(buffers.get(13));
		
		//visualize it:
		
//		Mat temp = Mat.zeros(IMG_HEIGHT, IMG_WIDTH, CvType.CV_8U);
//		for (int i = 0; i < wallYVals.length; i++) {
//			temp.put((int)wallYVals[i],i, 255.0);
//		}
//		temp.copyTo(processedFrame);
		
		
		blobs.put("red", findBlobs(buffers.get(5),wallYVals));
		blobs.put("green", findBlobs(buffers.get(6),wallYVals));
//		blobs.put("blue", findWalls(buffers.get(7).submat(0, 470, 280, 360))); 
		
		List<double[]> reactorWall = findWalls(buffers.get(8), wallYVals);
		if (reactorWall.size() > 0) {
			blobs.put("teal", reactorWall.subList(0, 1));
		} else {
			blobs.put("teal", reactorWall);
		}
		
		List<double[]> yellowWall = findWalls(buffers.get(10), wallYVals);
		if (yellowWall.size() > 0) {
			blobs.put("yellow", yellowWall.subList(0, 1));
		} else {
			blobs.put("yellow", yellowWall);
		}
		
		if (wallYVals.length == IMG_WIDTH) {
			double total = 0.0;
			List<double[]> wallEnds = new ArrayList<double[]>();
			double[] ends = new double[2];
			for (int i = 0; i < 10; i++) {
				total += wallYVals[i];
			}
			ends[0] = total / 10.0;
			total = 0.0;
			for (int i = 1; i <= 10; i++) {
				total += wallYVals[IMG_WIDTH - i];
			}
			ends[1] = total / 10.0;
			wallEnds.add(ends);
			blobs.put("wallEnds", wallEnds);
		} else {
			blobs.put("wallEnds", new ArrayList<double[]>());
		}
		
		return blobs;
	}
	
	
	//returns list of blobs' centers (x,y)
	public List<double[]> findBlobs(Mat binaryImg, double[] wallY) {
//		if (wallY > 0.0) {
//			binaryImg = binaryImg.submat((int)wallY, IMG_HEIGHT, 0, IMG_WIDTH);
//		}
		List<MatOfPoint> contours = new ArrayList<MatOfPoint>();
		Imgproc.findContours(binaryImg, contours, new Mat(), Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);
		List<double[]> blobs = new ArrayList<double[]>();
		for (MatOfPoint cnt : contours) {
			if (Imgproc.contourArea(cnt) > contourAreaThresh) {
				Rect bound = Imgproc.boundingRect(cnt);
				double x = bound.x + (bound.width / 2.0);
				double y = bound.y + (bound.height / 2.0);
				if (bound.y > wallY[(int)x]) {
					blobs.add(new double[] {x,y});
				}
//				blobs.add(new double[] {bound.x + (bound.width / 2.0), bound.y + (bound.height / 2.0) + wallY});
			}
		}
		return blobs;
	}
	
	public double[] findWallY(Mat binaryImg) {
		double[] ret = new double[IMG_WIDTH];
		double[] pix = {};
		int max = 0;
		for (int i = 0; i < IMG_WIDTH; i++) {
			for (int j = IMG_HEIGHT - 1; j >= 0; j--) {
				pix = binaryImg.get(j,i);
				if (pix.length > 0 && pix[0] > 0.5) {
					ret[i] = j;
					if (j > max) max = j;
					break;
				}
			}
		}
		for (int i = 0; i < IMG_WIDTH; i++) {
			if (ret[i] == 0) // if something weird happened and we don't have a wall pixel in this column
				ret[i] = max;
		}
		return ret;
	}
	
	// for walls, instead of returning the center, return the lower edge y
	// use the wallY to define a lower edge bound
	public List<double[]> findWalls(Mat binaryImg, double[] wallY) {
		List<MatOfPoint> contours = new ArrayList<MatOfPoint>();
		Imgproc.findContours(binaryImg, contours, new Mat(), Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);
		List<double[]> wall = new ArrayList<double[]>();
		Rect bestbound = null;
		for (int i = 0; i < contours.size(); i++) {
			MatOfPoint cnt = contours.get(i);
			if (Imgproc.contourArea(cnt) > contourAreaThresh*2) {
				Rect bound = Imgproc.boundingRect(cnt);
				if (bestbound == null || bound.y > bestbound.y) {
					// check against wallY
					if (bound.y + bound.height + 2 >= wallY[(int)(bound.x + bound.width / 2)]) {
						bestbound = bound;
					}
				}
			}
		}
		if (bestbound != null) {
			wall.add(new double[] {bestbound.x + (bestbound.width / 2.0), bestbound.y + bestbound.height, bestbound.width, bestbound.height});
			wall.add(new double[] {bestbound.y + (bestbound.height / 2.0)});
		}
		return wall;
	}
	
	
	private static void loadLibrary() {
	    try {
	        InputStream in = null;
	        File fileOut = null;
	        String osName = System.getProperty("os.name");
	        System.out.println(osName);
	        if(osName.startsWith("Windows")){
	            int bitness = Integer.parseInt(System.getProperty("sun.arch.data.model"));
	            if(bitness == 32){
	                System.out.println("32 bit detected");
	                in = FrameProcessor.class.getResourceAsStream("/opencv/x86/opencv_java248.dll");
	                fileOut = File.createTempFile("lib", ".dll");
	            }
	            else if (bitness == 64){
	                System.out.println("64 bit detected");
	                in = FrameProcessor.class.getResourceAsStream("/opencv/x64/opencv_java248.dll");
	                fileOut = File.createTempFile("lib", ".dll");
	            }
	            else{
	                System.out.println("Unknown bit detected - trying with 32 bit");
	                in = FrameProcessor.class.getResourceAsStream("/opencv/x86/opencv_java248.dll");
	                fileOut = File.createTempFile("lib", ".dll");
	            }
	        }
	        else if(osName.equals("Mac OS X")){
	            in = FrameProcessor.class.getResourceAsStream("/opencv/mac/libopencv_java248.dylib");
	            fileOut = File.createTempFile("lib", ".dylib");
	        }


	        OutputStream out = FileUtils.openOutputStream(fileOut);
	        if (out == null) System.out.println("out is null");
	        if (in == null) System.out.println("in is null");
	        IOUtils.copy(in, out);
	        in.close();
	        out.close();
	        System.load(fileOut.toString());
	    } catch (Exception e) {
	        throw new RuntimeException("Failed to load opencv native library", e);
	    }
	}
	
	/**
	 * main method just for testing purposes
	 */
	public static void main(String[] args) {
		//
	}

}
