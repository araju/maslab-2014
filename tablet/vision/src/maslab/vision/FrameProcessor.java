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

	private static final Scalar lowerBlue = new Scalar(90, 100, 50);
	private static final Scalar upperBlue = new Scalar(115, 255, 255);
	
	private static final Scalar lowerGreen = new Scalar(55, 80, 10);
	private static final Scalar upperGreen = new Scalar(90, 255, 255);
	
	private static final Scalar lowerRed = new Scalar(0, 100, 10);
	private static final Scalar upperRed = new Scalar(15, 255, 255);
	
	private static final int contourAreaThresh = 50;
	private static final int cleanKernelSize = 5;
	private static final int numBuffers = 7; //0: HSV, 1: Red Thresh, 2: Green, 3: Blue
											 // 4,5,6: cleaned Red, Green, Blue
	
	//TODO: add QR detection
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

	
	// returns map of color to list of blobs
	public Map<String,List<double[]>> processFrame(Mat frame) {
		//first convert to hsv, store it in the first buffer
		Imgproc.cvtColor(frame, buffers.get(0), Imgproc.COLOR_BGR2HSV);
		Core.inRange(buffers.get(0), lowerRed, upperRed, buffers.get(1));
		Core.inRange(buffers.get(0), lowerGreen, upperGreen, buffers.get(2));
		Core.inRange(buffers.get(0), lowerBlue, upperBlue, buffers.get(3));
		
		//clean thresholded images
		for (int i = 1; i <= 3; i++)
			Imgproc.morphologyEx(buffers.get(i), buffers.get(i+3), Imgproc.MORPH_OPEN, cleanKernel);
		
		Map<String,List<double[]>> blobs = new HashMap<String, List<double[]>>();
		blobs.put("red", findBlobs(buffers.get(4)));
		blobs.put("green", findBlobs(buffers.get(5)));
		blobs.put("blue", findBlobs(buffers.get(6)));
		
		return blobs;
	}
	
	
	//returns list of blobs' centers (x,y)
	public List<double[]> findBlobs(Mat binaryImg) {
		List<MatOfPoint> contours = new ArrayList<MatOfPoint>();
		Imgproc.findContours(binaryImg, contours, null, Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);
		List<double[]> blobs = new ArrayList<double[]>();
		for (MatOfPoint cnt : contours) {
			if (Imgproc.contourArea(cnt) > contourAreaThresh) {
				Rect bound = Imgproc.boundingRect(cnt);
				blobs.add(new double[] {bound.x + (bound.width / 2.0), bound.y + (bound.height / 2.0)});
			}
		}
		return blobs;
	}
	
	/**
	 * main method just for testing purposes
	 */
	public static void main(String[] args) {
		//
	}

}