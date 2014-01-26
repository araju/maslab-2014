package maslab.vision;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.imgproc.Imgproc;

public class FrameProcessor {

//	private static final Scalar lowerBlue = new Scalar(90, 100, 50);
//	private static final Scalar upperBlue = new Scalar(115, 255, 255);
	
//	private static final Scalar lowerGreen = new Scalar(55, 80, 10);
//	private static final Scalar upperGreen = new Scalar(90, 255, 255);
	
//	private static final Scalar lowerRed = new Scalar(0, 100, 10);
//	private static final Scalar upperRed = new Scalar(15, 255, 255);
	
	private static final int IMG_HEIGHT = 480;
	private static final int IMG_WIDTH = 640;
	
	private static final Scalar lowerRed = new Scalar(110, 100, 10);
	private static final Scalar upperRed = new Scalar(140, 255, 255);
	
	private static final Scalar lowerGreen = new Scalar(35, 80, 10);
	private static final Scalar upperGreen = new Scalar(60, 255, 255);
	
	private static final Scalar lowerBlue = new Scalar(0, 100, 50);
	private static final Scalar upperBlue = new Scalar(20, 255, 255);
	
	private static final Scalar lowerTeal = new Scalar(20, 100, 50);
	private static final Scalar upperTeal = new Scalar(33, 255, 255);
	
	private static final int contourAreaThresh = 50;
	private static final int cleanKernelSize = 5;
	private static final int numBuffers = 9; //0: HSV, 1: Red Thresh, 2: Green, 3: Blue, 4: Teal
											 // 5,6,7,8: cleaned Red, Green, Blue, Teal
	
	//TODO: do not detect above the lowest blue
	
	private List<Mat> buffers = null;
	private Mat cleanKernel;
	
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
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
		//first convert to hsv, store it in the first buffer
		Imgproc.cvtColor(frame, buffers.get(0), Imgproc.COLOR_BGR2HSV);
		Core.inRange(buffers.get(0), lowerRed, upperRed, buffers.get(1));
		Core.inRange(buffers.get(0), lowerGreen, upperGreen, buffers.get(2));
		Core.inRange(buffers.get(0), lowerBlue, upperBlue, buffers.get(3));
		Core.inRange(buffers.get(0), lowerTeal, upperTeal, buffers.get(4));
		
		//clean thresholded images
		Imgproc.morphologyEx(buffers.get(1), buffers.get(5), Imgproc.MORPH_OPEN, cleanKernel);
		Imgproc.morphologyEx(buffers.get(2), processedFrame, Imgproc.MORPH_OPEN, cleanKernel);
		Imgproc.morphologyEx(buffers.get(3), buffers.get(7), Imgproc.MORPH_OPEN, cleanKernel);
		Imgproc.morphologyEx(buffers.get(4), buffers.get(8), Imgproc.MORPH_OPEN, cleanKernel);
		buffers.set(6, processedFrame);
		
		Map<String,List<double[]>> blobs = new HashMap<String, List<double[]>>();
		List<double[]> wall = findWalls(buffers.get(7).submat(0, 470, 280, 360)); // WARNING: USING FIXED NUMBERS!!!
		double wallY = 0.0;
		if (wall.size() > 0) {
			blobs.put("blue", wall.subList(0, 1));
			wallY = wall.get(1)[0];
		} else {
			blobs.put("blue", wall);
		}
		
		blobs.put("red", findBlobs(buffers.get(5),wallY));
		blobs.put("green", findBlobs(buffers.get(6),wallY));
//		blobs.put("blue", findWalls(buffers.get(7).submat(0, 470, 280, 360))); 
		
		List<double[]> reactorWall = findWalls(buffers.get(8));
		if (reactorWall.size() > 0) {
			blobs.put("teal", reactorWall.subList(0, 1));
		} else {
			blobs.put("teal", reactorWall);
		}
		
		return blobs;
	}
	
	
	//returns list of blobs' centers (x,y)
	public List<double[]> findBlobs(Mat binaryImg, double wallY) {
		if (wallY > 0.0) {
			binaryImg = binaryImg.submat((int)wallY, IMG_HEIGHT, 0, IMG_WIDTH);
		}
		List<MatOfPoint> contours = new ArrayList<MatOfPoint>();
		Imgproc.findContours(binaryImg, contours, new Mat(), Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);
		List<double[]> blobs = new ArrayList<double[]>();
		for (MatOfPoint cnt : contours) {
			if (Imgproc.contourArea(cnt) > contourAreaThresh) {
				Rect bound = Imgproc.boundingRect(cnt);
				blobs.add(new double[] {bound.x + (bound.width / 2.0), bound.y + (bound.height / 2.0) + wallY});
			}
		}
		return blobs;
	}
	
	// this is specifically for the blue walls. instead of returning the center, return the lower edge y
	public List<double[]> findWalls(Mat binaryImg) {
		List<MatOfPoint> contours = new ArrayList<MatOfPoint>();
		Imgproc.findContours(binaryImg, contours, new Mat(), Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);
		List<double[]> wall = new ArrayList<double[]>();
		Rect bestbound = null;
		for (int i = 0; i < contours.size(); i++) {
			MatOfPoint cnt = contours.get(i);
			if (Imgproc.contourArea(cnt) > contourAreaThresh*2) {
				Rect bound = Imgproc.boundingRect(cnt);
				if (bestbound == null || bound.y > bestbound.y) {
					bestbound = bound;
				}
			}
		}
		if (bestbound != null) {
			wall.add(new double[] {bestbound.x + (bestbound.width / 2.0), bestbound.y + bestbound.height});
			wall.add(new double[] {bestbound.y + (bestbound.height / 2.0)});
		}
		return wall;
	}
	
	/**
	 * main method just for testing purposes
	 */
	public static void main(String[] args) {
		//
	}

}
